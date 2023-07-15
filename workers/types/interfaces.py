import dataclasses


@dataclasses.dataclass
class InterfaceLogin:
    ksignInputMberId: str = ""
    loginType: str = "idpw"
    failResult: str = ""
    cffdnCd: str = ""
    callCd: str = ""
    loginId: str = ""
    loginPwd: str = "Marat12!"
    captchaTxt: str = ""


@dataclasses.dataclass
class InterfaceCalendarData:
    emblCd: str
    visitResveBussGrpCd: str
    emblTime: str


@dataclasses.dataclass
class InterfaceReservationData:
    visitDe: str
    resveTimeNm: str
    timeCd: str
    visitResveId: str
    remk: str
    captchaTxt: str = ""
    emblCd: str = "GR"
    businessNm: str = "{\"mainKindNm\":[\"비자 접수\"],\"cffdnNm\":[\"비자 접수\"]}"
    grpNmListDB: str = "비자 접수"
    cffdnNmDB: str = "비자 접수"
    mainKind: str = "GR0001"
    subKind: str = "GR0001"
    natnCd: str = "130"
    totcnt: int = 1
    onedaycnt: int = 1


# {
#     "visitYn": "A",
#     "emblCd": "KY",
#     "visitDe": "20230901"
# },


@dataclasses.dataclass
class InterfaceReservationParams:
    visitResveBussGrpCd: str
    emblCd: str
    visitDe: str
