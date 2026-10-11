"""
Họ và tên: Hà Văn Mạnh
MSSV: 202418941
"""

from abc import ABC, abstractmethod
from datetime import date
from enum import Enum
from typing import Optional


class DeviceStatus(Enum):
    ACTIVE = "Active"
    UNDER_MAINTENANCE = "UnderMaintenance"
    RETIRED = "Retired"


class PrinterType(Enum):
    LASER = "Laser"
    INKJET = "Inkjet"


class INetworkable(ABC):
    """Interface quy dinh hanh vi cua thiet bi co kha nang ket noi mang."""

    @property
    @abstractmethod
    def IpAddress(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def IsConnected(self) -> bool:
        pass

    @abstractmethod
    def Connect(self, ip_address: str) -> None:
        pass

    @abstractmethod
    def Disconnect(self) -> None:
        pass


class Device(ABC):
    """Lop co so truu tuong cho moi thiet bi."""

    def __init__(
        self,
        device_id: str,
        name: str,
        year_introduced: int,
        purchase_price: float,
        status: DeviceStatus = DeviceStatus.ACTIVE,
    ):
        if not device_id or not device_id.strip():
            raise ValueError("Ma thiet bi khong duoc rong.")
        if purchase_price <= 0:
            raise ValueError("Gia mua phai lon hon 0.")
        if year_introduced > date.today().year:
            raise ValueError("Nam dua vao su dung khong duoc lon hon nam hien tai.")
        if not isinstance(status, DeviceStatus):
            raise ValueError("Trang thai thiet bi khong hop le.")

        # Ma thiet bi chi duoc gan khi khoi tao.
        self._device_id = device_id.strip()
        self.name = name
        self.year_introduced = year_introduced
        self.purchase_price = float(purchase_price)
        self.status = status

    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def years_used(self) -> int:
        return date.today().year - self.year_introduced

    @abstractmethod
    def CalculateAnnualMaintenanceCost(self) -> float:
        """Tra ve chi phi bao tri du kien trong mot nam."""
        pass

    def ToString(self) -> str:
        return (
            f"Ma: {self.device_id}, Ten: {self.name}, "
            f"Nam su dung: {self.year_introduced}, "
            f"Gia mua: {self.purchase_price:,.0f} VND, "
            f"Trang thai: {self.status.value}"
        )

    def __str__(self) -> str:
        return self.ToString()


class Computer(Device, INetworkable):
    def __init__(
        self,
        device_id: str,
        name: str,
        year_introduced: int,
        purchase_price: float,
        ram_capacity: int,
        processor_type: str,
        has_dedicated_gpu: bool,
        status: DeviceStatus = DeviceStatus.ACTIVE,
    ):
        super().__init__(device_id, name, year_introduced, purchase_price, status)
        if ram_capacity <= 0:
            raise ValueError("Dung luong RAM phai lon hon 0.")
        self.ram_capacity = ram_capacity
        self.processor_type = processor_type
        self.has_dedicated_gpu = has_dedicated_gpu
        self._ip_address: Optional[str] = None

    def CalculateAnnualMaintenanceCost(self) -> float:
        cost = self.purchase_price * 0.05
        if self.has_dedicated_gpu:
            cost += self.purchase_price * 0.02
        if self.years_used > 5:
            cost += self.purchase_price * 0.01
        return cost

    @property
    def IpAddress(self) -> Optional[str]:
        return self._ip_address

    @property
    def IsConnected(self) -> bool:
        return self._ip_address is not None

    def Connect(self, ip_address: str) -> None:
        if not ip_address or not ip_address.strip():
            raise ValueError("Dia chi IP khong duoc rong.")
        if self.IsConnected:
            raise RuntimeError(f"Thiet bi {self.device_id} dang ket noi mang.")
        self._ip_address = ip_address.strip()

    def Disconnect(self) -> None:
        self._ip_address = None

    def ToString(self) -> str:
        return (
            f"{super().ToString()}, RAM: {self.ram_capacity} GB, "
            f"CPU: {self.processor_type}, GPU roi: "
            f"{'Co' if self.has_dedicated_gpu else 'Khong'}"
        )


class Printer(Device):
    def __init__(
        self,
        device_id: str,
        name: str,
        year_introduced: int,
        purchase_price: float,
        printer_type: PrinterType,
        pages_printed: int,
        is_color: bool,
        supports_network: bool = False,
        status: DeviceStatus = DeviceStatus.ACTIVE,
    ):
        super().__init__(device_id, name, year_introduced, purchase_price, status)
        if pages_printed < 0:
            raise ValueError("So trang da in khong duoc am.")
        self.printer_type = printer_type
        self.pages_printed = pages_printed
        self.is_color = is_color
        self.supports_network = supports_network

    def CalculateAnnualMaintenanceCost(self) -> float:
        cost = self.purchase_price * 0.04
        if self.pages_printed > 100_000:
            cost += 500_000
        if self.is_color:
            cost += 300_000
        return cost

    def ToString(self) -> str:
        return (
            f"{super().ToString()}, Loai may in: {self.printer_type.value}, "
            f"So trang da in: {self.pages_printed:,}, "
            f"May in mau: {'Co' if self.is_color else 'Khong'}, "
            f"Ho tro mang: {'Co' if self.supports_network else 'Khong'}"
        )


class NetworkPrinter(Printer, INetworkable):
    """May in co kha nang ket noi mang."""

    def __init__(
        self,
        device_id: str,
        name: str,
        year_introduced: int,
        purchase_price: float,
        printer_type: PrinterType,
        pages_printed: int,
        is_color: bool,
        status: DeviceStatus = DeviceStatus.ACTIVE,
    ):
        super().__init__(
            device_id=device_id,
            name=name,
            year_introduced=year_introduced,
            purchase_price=purchase_price,
            printer_type=printer_type,
            pages_printed=pages_printed,
            is_color=is_color,
            supports_network=True,
            status=status,
        )
        self._ip_address: Optional[str] = None

    @property
    def IpAddress(self) -> Optional[str]:
        return self._ip_address

    @property
    def IsConnected(self) -> bool:
        return self._ip_address is not None

    def Connect(self, ip_address: str) -> None:
        if not ip_address or not ip_address.strip():
            raise ValueError("Dia chi IP khong duoc rong.")
        if self.IsConnected:
            raise RuntimeError(f"Thiet bi {self.device_id} dang ket noi mang.")
        self._ip_address = ip_address.strip()

    def Disconnect(self) -> None:
        self._ip_address = None


class Projector(Device):
    def __init__(
        self,
        device_id: str,
        name: str,
        year_introduced: int,
        purchase_price: float,
        brightness: int,
        lamp_hours_used: int,
        status: DeviceStatus = DeviceStatus.ACTIVE,
    ):
        super().__init__(device_id, name, year_introduced, purchase_price, status)
        if brightness <= 0:
            raise ValueError("Do sang phai lon hon 0 lumen.")
        if lamp_hours_used < 0:
            raise ValueError("So gio su dung bong den khong duoc am.")
        self.brightness = brightness
        self.lamp_hours_used = lamp_hours_used

    def CalculateAnnualMaintenanceCost(self) -> float:
        cost = self.purchase_price * 0.03
        if self.lamp_hours_used > 3_000:
            cost += 1_500_000
        return cost

    def ToString(self) -> str:
        return (
            f"{super().ToString()}, Do sang: {self.brightness} lumen, "
            f"So gio su dung bong den: {self.lamp_hours_used:,}"
        )


class LabRoom:
    """Quan ly danh sach thiet bi trong mot phong thuc hanh."""

    def __init__(self, room_id: str, room_name: str, capacity: int):
        if not room_id or not room_id.strip():
            raise ValueError("Ma phong khong duoc rong.")
        if capacity <= 0:
            raise ValueError("Suc chua phai lon hon 0.")
        self.room_id = room_id.strip()
        self.room_name = room_name
        self.capacity = capacity
        self.devices: list[Device] = []

    def AddDevice(self, device: Device) -> None:
        if device is None:
            raise ValueError("Khong the them thiet bi None.")
        if any(existing.device_id == device.device_id for existing in self.devices):
            raise ValueError(f"Phong {self.room_name} da co ma thiet bi {device.device_id}.")
        if len(self.devices) >= self.capacity:
            raise ValueError(f"Phong {self.room_name} da day.")
        self.devices.append(device)

    def RemoveDevice(self, device_id: str) -> bool:
        for device in self.devices:
            if device.device_id == device_id:
                self.devices.remove(device)
                return True
        return False

    def FindDevice(self, device_id: str) -> Optional[Device]:
        for device in self.devices:
            if device.device_id == device_id:
                return device
        return None

    def CalculateAnnualMaintenanceCost(self) -> float:
        # Da hinh: goi cung mot phuong thuc tren moi loai Device.
        return sum(device.CalculateAnnualMaintenanceCost() for device in self.devices)

    def GetDevicesRequiringMaintenance(self) -> list[Device]:
        return [
            device for device in self.devices
            if (
                device.status == DeviceStatus.UNDER_MAINTENANCE
                or device.years_used > 5
            )
        ]

    def PrintDevices(self) -> None:
        print(f"\nPhong {self.room_id} - {self.room_name}")
        if not self.devices:
            print("  (Chua co thiet bi)")
            return
        for device in self.devices:
            print(f"  - {device}")

    def __str__(self) -> str:
        return f"{self.room_id} - {self.room_name} (suc chua {self.capacity})"


def format_money(amount: float) -> str:
    return f"{amount:,.0f} VND"


def main() -> None:
    print("=== KHOI TAO THIET BI VA PHONG THUC HANH ===")

    # Tao 2 may tinh, trong do 1 may co GPU roi.
    computer1 = Computer(
        "PC001", "May tinh phong A", 2022, 20_000_000,
        ram_capacity=16, processor_type="Intel Core i5",
        has_dedicated_gpu=False,
    )
    computer2 = Computer(
        "PC002", "May tinh do hoa", 2019, 30_000_000,
        ram_capacity=32, processor_type="Intel Core i7",
        has_dedicated_gpu=True,
    )

    # Tao 2 may in, trong do 1 may da in tren 100.000 trang.
    printer1 = Printer(
        "PR001", "May in den trang", 2023, 5_000_000,
        printer_type=PrinterType.LASER,
        pages_printed=40_000, is_color=False,
    )
    printer2 = NetworkPrinter(
        "PR002", "May in mau co mang", 2020, 8_000_000,
        printer_type=PrinterType.INKJET,
        pages_printed=120_000, is_color=True,
    )

    # Tao 1 may chieu co bong den da su dung tren 3.000 gio.
    projector1 = Projector(
        "PJ001", "May chieu phong A", 2018, 15_000_000,
        brightness=4_000, lamp_hours_used=3_500,
    )

    # Tao 2 phong thuc hanh.
    room1 = LabRoom("R001", "Phong thuc hanh A", capacity=10)
    room2 = LabRoom("R002", "Phong thuc hanh B", capacity=10)

    print("\n=== 1. THEM THIET BI VAO PHONG ===")
    room1.AddDevice(computer1)
    room1.AddDevice(computer2)
    room1.AddDevice(printer1)
    room2.AddDevice(printer2)
    room2.AddDevice(projector1)
    print(f"Da them thiet bi vao {room1}")
    print(f"Da them thiet bi vao {room2}")

    print("\n=== 2. THU THEM THIET BI BI TRUNG MA ===")
    duplicate = Computer(
        "PC001", "May tinh trung ma", 2024, 12_000_000,
        ram_capacity=8, processor_type="Intel Core i3",
        has_dedicated_gpu=False,
    )
    try:
        room1.AddDevice(duplicate)
    except ValueError as error:
        print(f"Tu choi them thiet bi: {error}")

    print("\n=== 3. IN DANH SACH THIET BI TUNG PHONG ===")
    room1.PrintDevices()
    room2.PrintDevices()

    print("\n=== 4. TONG CHI PHI BAO TRI DU KIEN ===")
    for room in (room1, room2):
        print(
            f"{room.room_name}: "
            f"{format_money(room.CalculateAnnualMaintenanceCost())}"
        )

    print("\n=== 5. DANH SACH THIET BI CAN BAO TRI ===")
    for room in (room1, room2):
        print(f"\n{room.room_name}:")
        needing_maintenance = room.GetDevicesRequiringMaintenance()
        if not needing_maintenance:
            print("  Khong co thiet bi can bao tri.")
        else:
            for device in needing_maintenance:
                print(f"  - {device.device_id}: {device.name}")

    print("\n=== 6. KET NOI MANG CAC DOI TUONG INetworkable ===")
    network_devices: list[INetworkable] = [
        device
        for room in (room1, room2)
        for device in room.devices
        if isinstance(device, INetworkable)
    ]

    # Duyet qua interface, khong can viet rieng cho Computer/NetworkPrinter.
    for index, network_device in enumerate(network_devices, start=1):
        network_device.Connect(f"192.168.1.{100 + index}")
        print(
            f"Da ket noi: IP={network_device.IpAddress}, "
            f"IsConnected={network_device.IsConnected}"
        )

    print("\n=== 7. DUYET THIET BI MANG THONG QUA INetworkable ===")
    for network_device in network_devices:
        print(
            f"IP={network_device.IpAddress}, "
            f"IsConnected={network_device.IsConnected}"
        )

    print("\n=== KIEM TRA NGAT KET NOI ===")
    if network_devices:
        first_device = network_devices[0]
        first_device.Disconnect()
        print(
            f"Sau khi ngat: IP={first_device.IpAddress}, "
            f"IsConnected={first_device.IsConnected}"
        )

    print("\n=== KIEM TRA THEM: KHONG CHO KET NOI LAI KHI DANG KET NOI ===")
    if len(network_devices) > 1:
        try:
            network_devices[1].Connect("192.168.1.250")
        except RuntimeError as error:
            print(f"Tu choi ket noi lai: {error}")


if __name__ == "__main__":
    main()
