from typing import List
from pydantic import BaseModel
from enum import Enum



class CalibrationData(BaseModel):
    id: str
    title: str
    value: str


class HardwareInfo(BaseModel):
    name: str
    title: str
    value: str

class ResourceTypeEnum(str, Enum):
    device = "hardware"
    emulator = "emulator"


class Resource(BaseModel):
    R_id: int
    name: str
    title: str
    processorType: str = "emulator"
    type: ResourceTypeEnum = ResourceTypeEnum.emulator
    status: bool
    basisGates: str
    qubits: int
    version: str
    qv : int = 0
    clops: float = 0
    medianCNOTError : float = 0
    medianSXError : float = 0
    medianReadoutError : float = 0
    medianT1 : float = 0
    medianT2 : float = 0
    instancesWithAccess : float = 0
    gates: List[str] = []
    hwInfo: List[HardwareInfo] = []
    calibrationDatas: List[List[CalibrationData]] = []

    def __return_status(self):
        if self.status:
            return "Online"
        else:
            return "Offline"

    def __basisGates_to_gates(self):
        return [s.strip() for s in self.basisGates.split(",")]

    def getDetail(self):
        if self.type == "emulator":
            return {
                "details": [
                    {
                        "name": "name",
                        "title": "Name",
                        "value": self.name,
                    },   
                    {
                        "name": "title",
                        "title": "Title",
                        "value": self.title,
                    },                    
                    {
                        "name": "version",
                        "title": "Version",
                        "value": self.version,
                    },
                    {
                        "name": "type",
                        "title": "Type",
                        "value": self.type,
                    },
                    {
                        "name": "status",
                        "title": "Status",
                        "value": self.__return_status(),
                    },
                    {
                        "name": "numberOfQibits",
                        "title": "Number of qubits",
                        "value": self.qubits,
                    },      
                    {
                        "name": "processorType",
                        "title": "Processor Type",
                        "value": self.processorType,
                    },
                    {
                        "name": "qv",
                        "title": "QV",
                        "value": None,
                    },
                    {"name": "clops", "title": "CLOPS", "value": None, "unit": "k"},
                    {
                        "name": "basisGates",
                        "title": "Basis gates",
                        "value": self.__basisGates_to_gates(),
                    },
                ],
            }
        else:
            return {
                "details": [
                    {
                        "name": "name",
                        "title": "Name",
                        "value": self.name,
                    },   
                    {
                        "name": "title",
                        "title": "Title",
                        "value": self.title,
                    },               
                    {
                        "name": "version",
                        "title": "Version",
                        "value": self.version,
                    },
                    {
                        "name": "type",
                        "title": "Type",
                        "value": self.type,
                    },
                    {
                        "name": "status",
                        "title": "Status",
                        "value": self.__return_status(),
                    },
                    {
                        "name": "numberOfQibits",
                        "title": "Number of qubits",
                        "value": self.qubits,
                    },
                    {
                        "name": "processorType",
                        "title": "Processor Type",
                        "value": self.processorType,
                    },
                    {
                        "name": "qv",
                        "title": "QV",
                        "value": self.qv,
                    },
                    {
                        "name": "clops",
                        "title": "Clops",
                        "value": self.clops,
                        "unit": "k"
                    },
                    {
                        "name": "medianCNOTError",
                        "title": "Median CNOT Error",
                        "value": self.medianCNOTError,
                    },

                    {
                        "name": "medianSXError",
                        "title": "Median SX Error",
                        "value": self.medianSXError,
                    },
                    {
                        "name": "medianReadoutError",
                        "title": "Median Readout Error",
                        "value": self.medianReadoutError,
                    },

                    {
                        "name": "medianT1",
                        "title": "Median T1",
                        "value": self.medianT1,
                        "unit": "us"
                    },
                    {
                        "name": "medianT2",
                        "title": "Median T2",
                        "value": self.medianT2,
                        "unit": "us"
                    },
                    {
                        "name": "instancesWithAccess",
                        "title": "Instances With Access",
                        "value": self.instancesWithAccess,
                        "unit": "Instances"
                    },
                    {
                        "name": "basisGates",
                        "title": "Basis gates",
                        "value": self.__basisGates_to_gates(),
                    },
                ],
                "calibrationDatas": self.calibrationDatas,
            }

    def getStatus(self):
        return self.status

    def getName(self):
        return self.name

    def setStatus(self, status: bool):
        self.status = status
        return self.status
