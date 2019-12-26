import sys
import os
import argparse
import subprocess
import shutil

top_dir = os.path.abspath(os.path.dirname(__file__))


def parse_arguments():
    parser = argparse.ArgumentParser(description="Switch for quiet or loud mode")
    parser.add_argument('-q', '--quiet', action='store_true', help='Prevents from printing build result', default=False)
    return vars(parser.parse_args())['quiet']

def main():
    
    capture_output_flag = parse_arguments()

    if not os.path.isdir(top_dir + "/src"):
        print("Cannot find dir: src")
        return -1, capture_output_flag
    
    build_dir = top_dir + "/src/" + "build"
    if not os.path.isdir(build_dir):
        os.mkdir(build_dir)
    
    final_result = None
    with open(build_dir + "/logs.txt", "w") as file:
        result = subprocess.run(["cmake", ".."], cwd=build_dir, capture_output=capture_output_flag)
        file.write("CMAKE:\n\n")
        file.write("COMMAND: " + str(result.args) + "\n")
        file.write("RETURN CODE: " + str(result.returncode) + "\n")
        file.write("STDOUT: " + str(result.stdout).replace("\\n", "\n") + "\n")
        file.write("STDERR: " + str(result.stderr).replace("\\n", "\n") + "\n")

        if result.returncode != 0:
            return result.returncode

        result = subprocess.run(["make", "-j8"], cwd=build_dir, capture_output=capture_output_flag)
        file.write("BUILD:\n\n")
        file.write("COMMAND: " + str(result.args) + "\n")
        file.write("RETURN CODE: " + str(result.returncode) + "\n")
        file.write("STDOUT: " + str(result.stdout).replace("\\n", "\n") + "\n")
        file.write("STDERR: " + str(result.stderr).replace("\\n", "\n") + "\n")

        final_result = result.returncode
    
    if final_result == 0:
        shutil.copyfile(build_dir + "/cnn.so", top_dir + "/../Modules/cnn/cnn.so")
    return final_result, capture_output_flag


if __name__ == "__main__":
    exit_code, quiet_mode = main()
    if quiet_mode:
        if exit_code == 0:
            print("SUCCESS")
        else:
            print("FAILED - Check logs.txt for details")
    sys.exit(exit_code)