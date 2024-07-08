from app.models.resource import Resource, ResourceTypeEnum
from starlette.config import Config

config = Config(".env.local")


def csv_to_cal_info(filePath: str):
    import csv

    result = []
    f = open(filePath, "r", encoding="utf-8")
    rdr = csv.reader(f)
    for index, value in enumerate(rdr):
        if index == 0:
            title = value
        elif index == 1:
            id_value = value
        else:
            arr = []
            for idx, val in enumerate(value):
                arr.append({"id": id_value[idx], "title": title[idx], "value": val})
            result.append(arr)
    # print(result)
    f.close()
    return result


def create_kisti_emulator():
    return Resource(
        R_id=1,
        name=config("name"),
        type=ResourceTypeEnum.emulator,
        status=True,
        title=config("title"),
        version=config("version"),
        qubits=config("numberOfQibits"),
        basisGates=config("basisGates")
    )


def create_kriss_hardware():
    csv_filepath = config("calibrationDataFilePath")

    return Resource(
        R_id=2,
        name=config("title"),
        type=ResourceTypeEnum.device,
        status=True,
        title=config("title"),
        qubits=config("numberOfQibits"),
        basisGates=config("basisGates"),
        processorType=config("processorType"),
        version=config("version"),
        qv=config("qv"),
        clops=config("clops"),
        medianCNOTError=config("medianCNOTError"),
        medianSXError=config("medianSXError"),
        medianReadoutError=config("medianReadoutError"),
        medianT1=config("medianT1"),
        medianT2=config("medianT2"),
        instancesWithAccess=config("instancesWithAccess"),

        calibrationDatas=csv_to_cal_info(csv_filepath),
    )


def create_resource():
    resource_type = config("type")

    if resource_type == "emulator":
        return create_kisti_emulator()

    elif resource_type == "hardware":
        return create_kriss_hardware()


resource_info = create_resource()
