from pyniryo2 import *

if __name__ == "__main__":
    ned = NiryoRobot("169.254.200.201") # Assuming ethernet!
    ned.tool.open_gripper()
    ned.tool.close_gripper()
    d = dict()
    print("A1")
    input("<Enter to continue>")
    d["A1"] = ned.arm.get_joints()
    print("B1")
    input("<Enter to continue>")
    d["B1"] = ned.arm.get_joints()
    print("C1")
    ned.tool.open_gripper()
    input("<Enter to continue>")
    d["C1"] = ned.arm.get_joints()
    print(d)
