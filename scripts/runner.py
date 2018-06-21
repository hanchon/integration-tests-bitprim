import sys
import os
import subprocess
import tempfile
import time
import signal
import logging

SCRIPTS_DIR = "./"
MY_NAME = "runner.py"
TEST_DBS_DIR = "./temp"
BITPRIM_BN_FOLDER = "./"
BITPRIM_BN_NAME = "bn"

# Formatting. Default colors to empty strings.
BOLD, BLUE, RED, GREY = ("", ""), ("", ""), ("", ""), ("", "")
try:
    # Make sure python thinks it can write unicode to its stdout
    "\u2713".encode("utf_8").decode(sys.stdout.encoding)
    TICK = "✓ "
    CROSS = "✖ "
    CIRCLE = "○ "
except UnicodeDecodeError:
    TICK = "P "
    CROSS = "x "
    CIRCLE = "o "

TEST_EXIT_PASSED = 0
TEST_EXIT_SKIPPED = 77


def on_ci():
    return os.getenv('TRAVIS') == 'true' or os.getenv('TEAMCITY_VERSION') != None


def get_all_scripts_from_disk(test_dir):
    python_files = set([t for t in os.listdir(test_dir) if t[-3:] == ".py"])
    return list(python_files - set({MY_NAME}))


def kill_old_executions():
    try:
        pidofOutput = subprocess.check_output(["pidof", BITPRIM_BN_NAME])
        ids = [int(i) for i in pidofOutput.decode('utf-8').rstrip().split()]
        for id in ids:
            os.kill(id, signal.SIGKILL)
        time.sleep(1)
    except (OSError, subprocess.SubprocessError):
        return True

    try:
        newpid = subprocess.check_output(["pidof", BITPRIM_BN_NAME])
        return False
    except (OSError, subprocess.SubprocessError):
        return True


def delete_old_execution():
    while not kill_old_executions():
        time.sleep(1)
    os.system('rm -rf ' + TEST_DBS_DIR)


def print_results(test_results, max_len_name, runtime):
    results = "\n" + BOLD[1] + "%s | %s | %s\n\n" % (
        "TEST".ljust(max_len_name), "STATUS   ", "DURATION") + BOLD[0]

    test_results.sort(key=lambda result: result.name.lower())
    all_passed = True
    time_sum = 0

    for test_result in test_results:
        all_passed = all_passed and test_result.status != "Failed"
        time_sum += test_result.time
        test_result.padding = max_len_name
        results += str(test_result)

    status = TICK + "Passed" if all_passed else CROSS + "Failed"
    results += BOLD[1] + "\n%s | %s | %s s (accumulated) \n" % (
        "ALL".ljust(max_len_name), status.ljust(9), time_sum) + BOLD[0]
    results += "Runtime: %s s\n" % (runtime)
    print(results)


class TestResult():
    def __init__(self, name, status, time, stdout, stderr):
        self.name = name
        self.status = status
        self.time = time
        self.padding = 0
        self.stdout = stdout
        self.stderr = stderr

    def __repr__(self):
        if self.status == "Passed":
            color = BLUE
            glyph = TICK
        elif self.status == "Failed":
            color = RED
            glyph = CROSS
        elif self.status == "Skipped":
            color = GREY
            glyph = CIRCLE

        return color[1] + "%s | %s%s | %s s\n" % (
            self.name.ljust(self.padding), glyph, self.status.ljust(7), self.time) + color[0]


class TestHandler:
    """
    Trigger the testscrips passed in via the list.
    """

    def __init__(self, tests_dir, test_list=None):

        self.num_jobs = 1
        self.tests_dir = tests_dir
        self.test_list = test_list
        self.num_running = 0
        self.jobs = []

    def get_next(self):
        while self.num_running < self.num_jobs and self.test_list:
            delete_old_execution()
            # Add tests
            self.num_running += 1
            t = self.test_list.pop(0)
            log_stdout = tempfile.SpooledTemporaryFile(max_size=2 ** 16)
            log_stderr = tempfile.SpooledTemporaryFile(max_size=2 ** 16)
            self.jobs.append((t,
                              time.time(),
                              subprocess.Popen([os.path.join(self.tests_dir, t)], universal_newlines=True,
                                               stdout=log_stdout, stderr=log_stderr),
                              log_stdout,
                              log_stderr))
        if not self.jobs:
            raise IndexError('pop from empty list')
        while True:
            # Return first proc that finishes
            time.sleep(.5)
            for j in self.jobs:
                (name, time0, proc, log_out, log_err) = j
                if on_ci() and int(time.time() - time0) > 10 * 60:
                    # In travis, timeout individual tests after 10 minutes
                    proc.send_signal(signal.SIGINT)
                if proc.poll() is not None:
                    log_out.seek(0), log_err.seek(0)
                    [stdout, stderr] = [l.read().decode('utf-8') for l in (log_out, log_err)]
                    log_out.close(), log_err.close()
                    if proc.returncode == TEST_EXIT_PASSED and stderr == "":
                        status = "Passed"
                    elif proc.returncode == TEST_EXIT_SKIPPED:
                        status = "Skipped"
                    else:
                        status = "Failed"
                    self.num_running -= 1
                    self.jobs.remove(j)

                    return TestResult(name, status, int(time.time() - time0), stdout, stderr)
            print('.', end='', flush=True)


def run_tests(tests_dir, test_list):
    # Set env vars
    if "BITPRIM" not in os.environ:
        os.environ["BITPRIM"] = "" + str(BITPRIM_BN_FOLDER) + str(BITPRIM_BN_NAME)

    max_len_name = len(max(test_list, key=len))

    # Run Tests
    job_queue = TestHandler(tests_dir, test_list)
    time0 = time.time()
    test_results = []

    for _ in range(len(test_list)):
        test_result = job_queue.get_next()
        test_results.append(test_result)

        if test_result.status == "Passed":
            logging.debug("\n%s%s%s passed, Duration: %s s" % (
                BOLD[1], test_result.name, BOLD[0], test_result.time))
        elif test_result.status == "Skipped":
            logging.debug("\n%s%s%s skipped" %
                          (BOLD[1], test_result.name, BOLD[0]))
        else:
            print("\n%s%s%s failed, Duration: %s s\n" %
                  (BOLD[1], test_result.name, BOLD[0], test_result.time))
            print(BOLD[1] + 'stdout:\n' + BOLD[0] + test_result.stdout + '\n')
            print(BOLD[1] + 'stderr:\n' + BOLD[0] + test_result.stderr + '\n')

    runtime = int(time.time() - time0)
    print_results(test_results, max_len_name, runtime)

    # Clear up the temp directory if all subdirectories are gone
    if not os.listdir(TEST_DBS_DIR):
        os.rmdir(TEST_DBS_DIR)

    all_passed = all(map(lambda test_result: test_result.status == "Passed", test_results))

    sys.exit(not all_passed)


def main():
    all_scripts = get_all_scripts_from_disk(SCRIPTS_DIR)
    run_tests(SCRIPTS_DIR, all_scripts)


if __name__ == '__main__':
    main()
