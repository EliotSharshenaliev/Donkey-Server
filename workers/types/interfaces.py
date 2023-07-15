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
    emblCd: str = "KY"
    businessNm: str = "{\"mainKindNm\":[\"비자 접수\"],\"cffdnNm\":[\"비자 접수\"]}"
    grpNmListDB: str = "비자 접수"
    cffdnNmDB: str = "비자 접수"
    mainKind: str = "KY0001"
    subKind: str = "KY0001"
    natnCd: str = "130"
    totcnt: int = 1
    onedaycnt: int = 1


@dataclasses.dataclass
class InterfaceReservationParams:
    visitResveBussGrpCd: str
    emblCd: str
    visitDe: str
