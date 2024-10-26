from utils.response import Response
from utils.status import Status


class System:
    def start(self) -> Response[str]:
        return Response(Status.OK,"",1)
