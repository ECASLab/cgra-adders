def load_config(dut_name):
    module = __import__(f'dut.{dut_name}.config', fromlist=['CONFIG'])

    return module.CONFIG
