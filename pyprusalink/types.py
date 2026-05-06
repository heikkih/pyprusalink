from enum import Enum
from typing import TypedDict

"""Types of the v1 API. Source: https://github.com/prusa3d/Prusa-Link-Web/blob/master/spec/openapi.yaml"""


class PrusaLinkError(Exception):
    """Base class for PrusaLink errors."""


class InvalidAuth(PrusaLinkError):
    """Error to indicate there is invalid auth."""


class Conflict(PrusaLinkError):
    """Error to indicate the command hit a conflict."""


class NotFound(PrusaLinkError):
    """Error to indicate the requested resource was not found. (404)"""


class Capabilities(TypedDict):
    """API Capabilities"""

    upload_by_put: bool | None


class VersionInfo(TypedDict):
    """Version data from /api/version.

    Field availability differs between PrusaLink variants and firmware versions:

    Bundled PrusaLink (Prusa-Firmware-Buddy, all printers):
      Always returned: api, server, nozzle_diameter, text, hostname, capabilities
      Returned on v6.5.1+ only: firmware, printer
        - v6.5.1 (2025-11-11): added on Core One L
        - v6.5.3 (2026-03-24): propagated to Core One/MK4/MK3.9/MK3.5 family
        - XL (6.4.x track) and MINI (6.4.0): not yet backported
        - Source: https://github.com/prusa3d/Prusa-Firmware-Buddy/commit/64b7a21

    Standalone PrusaLink (RPi-based installations):
      May return version and sdk per the Prusa-Link-Web OpenAPI spec; these
      are never returned by bundled firmware.

    Use dict.get() for any field other than `api` to handle absence safely.
    """

    api: str
    text: str | None
    server: str | None
    hostname: str | None
    nozzle_diameter: float | None
    firmware: str | None
    printer: str | None
    version: str | None
    sdk: str | None
    capabilities: Capabilities | None


class PrinterInfo(TypedDict):
    """Printer informations."""

    mmu: bool | None
    name: str | None
    location: str | None
    farm_mode: bool | None
    nozzle_diameter: float | None
    min_extrusion_temp: int | None
    serial: str | None
    sd_ready: bool | None
    active_camera: bool | None
    hostname: str | None
    port: str | None
    network_error_chime: bool | None


class StatusInfo(TypedDict):
    """Status of the printer."""

    ok: bool | None
    message: str | None


class PrinterState(Enum):
    """Printer state as Enum."""

    IDLE = "IDLE"
    BUSY = "BUSY"
    PRINTING = "PRINTING"
    PAUSED = "PAUSED"
    FINISHED = "FINISHED"
    STOPPED = "STOPPED"
    ERROR = "ERROR"
    ATTENTION = "ATTENTION"
    READY = "READY"


class PrinterStatusInfo(TypedDict):
    """Printer information."""

    state: PrinterState
    temp_nozzle: float | None
    target_nozzle: float | None
    temp_bed: float | None
    target_bed: float | None
    axis_x: float | None
    axis_y: float | None
    axis_z: float | None
    flow: int | None
    speed: int | None
    fan_hotend: int | None
    fan_print: int | None
    status_printer: StatusInfo | None
    status_connect: StatusInfo | None


class PrinterStatus(TypedDict):
    """Printer status."""

    printer: PrinterStatusInfo


class PrintFileRefs(TypedDict):
    """Additional Files for the current Job"""

    download: str | None
    icon: str | None
    thumbnail: str | None


class JobFilePrint(TypedDict):
    """Currently printed file informations."""

    name: str
    display_name: str | None
    path: str
    display_path: str | None
    size: int | None
    m_timestamp: int
    meta: dict | None
    refs: PrintFileRefs | None


class JobInfo(TypedDict):
    """Job information."""

    id: int
    state: str
    progress: int
    time_remaining: int | None
    time_printing: int
    inaccurate_estimates: bool | None
    serial_print: bool | None
    file: JobFilePrint | None
