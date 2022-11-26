import cy_kit
from cyx.images import ImageServices
from cyx.base import Base,Config
from cyx.contents import Contents
img_service = cy_kit.singleton(
    ImageServices
)
config:Config= cy_kit.singleton(
    Config
)
contents:Contents =cy_kit.singleton(
    Contents
)
config.load("./config.yml")
img_service.create_thumbs(
    image_file_path=r"C:\code\python\py_cy\test_resource\img_01.png",
    size=120
)
pdf_path = img_service.convert_to_pdf(image_file_path=r"C:\code\python\py_cy\test_resource\img_01.png")
a,b = contents.get_text(pdf_path)
print(a)
