import pathlib

import elasticsearch
import cy_kit
import cy_es
import cy_xdoc.configs
from cy_xdoc.services.text_procesors import TextProcessService
from cy_xdoc.services.file_content_extractors import FileContentExtractorService

class SearchEngine:
    def __init__(self,
                 text_process_service:TextProcessService = cy_kit.singleton(TextProcessService),
                 file_content_extractor_service:FileContentExtractorService = cy_kit.singleton(FileContentExtractorService)):
        self.config = cy_xdoc.configs.config
        self.client = elasticsearch.Elasticsearch(
            cy_xdoc.configs.config.elastic_search.server
        )
        self.prefix_index = cy_xdoc.configs.config.elastic_search.prefix_index
        self.text_process_service = text_process_service
        self.file_content_extractor_service=file_content_extractor_service

    def delete_index(self, app_name):
        self.client.indices.delete(index=self.get_index(app_name))
    def get_index(self, app_name):
        if app_name == "admin":
            app_name = self.config.admin_db_name
        return f"{self.prefix_index}_{app_name}"

    def delete_doc(self, app_name, id: str):
        return cy_es.delete_doc(
            client=self.client,
            index= self.get_index(app_name),
            id =id
        )


    def mark_delete(self, app_name, id, mark_delete_value):
        ret = cy_es.update_doc_by_id(
            client=self.client,
            id=id,
            index=self.get_index(app_name),
            data=(
                cy_es.buiders.mark_delete<<mark_delete_value,
            )
        )
        return ret

    def full_text_search(self, app_name, content, page_size: int, page_index: int, highlight: bool):
        search_expr = (cy_es.buiders.mark_delete == False) & cy_es.match(
            field=cy_es.buiders.content,
            content=content

        )
        skip = page_index * page_size
        highlight_expr = None
        if highlight:
            highlight_expr = cy_es.buiders.content
        ret = cy_es.search(
            client=self.client,
            limit=page_size,
            excludes=[
                cy_es.buiders.content,
                cy_es.buiders.meta_info,
                cy_es.buiders.vn_on_accent_content],
            index=self.get_index(app_name),
            highlight=highlight_expr,
            filter=search_expr,
            skip=skip

        )
        return ret

    def get_doc(self, app_name: str, id: str, doc_type: str = "_doc"):
        return cy_es.get_doc(client=self.client, id=id, doc_type=doc_type, index=self.get_index(app_name))

    def copy(self, app_name: str, from_id: str, to_id: str, attach_data, run_in_thread: bool = True):
        @cy_kit.thread_makeup()
        def copy_elastics_search(app_name: str, from_id: str, to_id: str, attach_data):
            es_doc = self.get_doc(id=from_id, app_name=app_name)
            if es_doc:
                es_doc.source.upload_id = to_id
                es_doc.source.data_item = attach_data
                es_doc.source["mark_delete"]=False
                ret =self.create_doc(app_name=app_name, id=to_id, body=es_doc.source)

        if run_in_thread:
            copy_elastics_search(app_name,  from_id,to_id, attach_data).start()
        else:
            copy_elastics_search(app_name,  from_id,to_id, attach_data).start().join()

    def create_doc(self, app_name, id:str, body):
        return cy_es.create_doc(
            client=self.client,
            index=self.get_index(app_name),
            id=id,
            body=body
        )

    def make_index_content(self, app_name: str, upload_id: str, data_item: dict,privileges:dict, path_to_file_content: str = None):
        if path_to_file_content is not None:
            content, meta_info = self.file_content_extractor_service.get_text(path_to_file_content)
            file_name = pathlib.Path(path_to_file_content).name
        else:
            content, meta_info = None,None
            file_name = None
        index_name = self.get_index(app_name)

        vn_on_accent_content = self.text_process_service.vn_clear_accent_mark(content)
        cy_es.create_doc(
            client=self.client,
            index=index_name,
            id=upload_id,
            body= dict(
                app_name=app_name,
                upload_id=upload_id,
                file_name=file_name,
                mark_delete=False,
                content=content,
                vn_on_accent_content=vn_on_accent_content,
                meta_info=meta_info,
                data_item=data_item,
                privileges=privileges
            )
        )

        del content
        del meta_info
        del vn_on_accent_content

    def create_or_update_privileges(self, app_name, upload_id, data_item: dict, privileges):
        doc = self.get_doc(app_name,id=upload_id)
        if doc:
            return cy_es.update_doc_by_id(
                client=self.client,
                index=self.get_index(app_name),
                id= upload_id,
                data = (
                    cy_es.buiders.privileges << privileges
                )
            )
        else:
            self.make_index_content(
                app_name=app_name,
                privileges=privileges,
                upload_id=upload_id,
                data_item=data_item
            )

