import subprocess

def run_auxiliary_function(values):
    """
    Runs auxiliary system functions, to better enrich the logs, or for other reasons
    :param values: values passed in the subprocesses.run() (array)
    :return:
    """
    result = subprocess.run(
        " ".join(values),
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout
