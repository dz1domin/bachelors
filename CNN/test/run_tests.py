import os
import cmd
import subprocess
import sys
import argparse

test_dirs = [
    'ModelConfig',
    'CNNBlurDetector'
]

top_dir = os.path.abspath(os.path.dirname(__file__))


def parse_arguments():
    parser = argparse.ArgumentParser(description="Switch for quiet or loud mode")
    parser.add_argument('-q', '--quiet', action='store_true', help='Prevents from printing tests result', default=False)
    return vars(parser.parse_args())['quiet']

def main():
    capture_output_flag = parse_arguments()
    final_result = 0
    for test_dir in test_dirs:
        build_dir = top_dir + "/" + test_dir + "/build"
        if not os.path.isdir(build_dir):
            os.mkdir(build_dir)

        with open(build_dir + "/logs.txt", "w") as file:

            result = subprocess.run(["cmake", ".."], cwd=build_dir, capture_output=capture_output_flag)
            file.write("BUILD:\n\n")
            file.write("COMMAND: " + str(result.args) + "\n")
            file.write("RETURN CODE: " + str(result.returncode) + "\n")
            file.write("STDOUT: " + str(result.stdout).replace("\\n", "\n") + "\n")
            file.write("STDERR: " + str(result.stderr).replace("\\n", "\n") + "\n")
            

            if result.returncode == 0:
                result = subprocess.run(["make","run"], cwd=build_dir, capture_output=capture_output_flag)
                file.write("TESTS:\n\n")
                file.write("COMMAND: " + str(result.args) + "\n")
                file.write("RETURN CODE: " + str(result.returncode) + "\n")
                file.write("STDOUT: " + str(result.stdout).replace("\\n", "\n") + "\n")
                file.write("STDERR: " + str(result.stderr).replace("\\n", "\n") + "\n")

                if result.returncode != 0:
                    final_result = result.returncode

            else:
                final_result = result.returncode
        
    return final_result, capture_output_flag

if __name__ == "__main__":
    exit_code, quiet_mode = main()
    if quiet_mode:
        if exit_code == 0:
            print("ALL TESTS PASSED")
        else:
            print("SOME TESTS FAILED -> CHECK LOGS FOR DETAILS")

    sys.exit(exit_code)