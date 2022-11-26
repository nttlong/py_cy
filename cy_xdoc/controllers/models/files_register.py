from typing import List, Union, Optional
from pydantic import Field, BaseModel
import cy_web


@cy_web.model(all_fields_are_optional=True)
class Error:
    """
    Thông tin chi tiết của lỗi
    """
    Code: str
    Message: str
    Fields: List[str]
@cy_web.model()
class PrivilegesType:
    Type:str
    Values:str
    """
    Separated by comma
    """
@cy_web.model()
class RegisterUploadInfo:
    """
    Bảng ghi thông tin đăng ký upload
    """
    FileName: str
    ChunkSizeInKB: int
    FileSize: int
    IsPublic: Optional[bool]
    ThumbConstraints: Optional[str]
    Privileges: Optional[List[PrivilegesType]]


@cy_web.model()
class RegisterUploadResult:
    NumOfChunks:int
    """
    Số phân đoạn: Rất quan trọng dùng để hỗ trợ __client__ upload 
    """
    ChunkSizeInBytes: int
    """
    Kích thước phân đoạn: Rất quan trọng dùng để hỗ trợ __client__ upload
    """
    UploadId: str
    """
    Upload Id: Hỗ trơ các ứng dụng khác lấy thông tin
    """
    ServerFilePath: str
    """
    Đường dẫn đến file tại server: Rất quan trọng các ứng dụng khác sẽ lưu lại thông tin này
    """
    MimeType: str
    """
    Mime type:: Rất quan trọng các ứng dụng khác sẽ lưu lại thông tin này
    """
    RelUrlOfServerPath: str
    SizeInHumanReadable: str
    UrlOfServerPath: str
    OriginalFileName: str
    """
    Tên file gốc lúc upload
    """
    UrlThumb: str
    """
    Đường dẫn đầy đủ đến ảnh Thumb
    """
    RelUrlThumb: str
    FileSize: int


@cy_web.model(all_fields_are_optional=True)
class RegisterUploadInfoResult:
    """
    Bảng ghi cấu trúc trả vể cho API upload
    """
    Data: RegisterUploadResult
    Error: Error
