
import { BaseScope, View } from "./../../js/ui/BaseScope.js";
//import { ui_rect_picker } from "../../js/ui/ui_rect_picker.js";
//import { ui_pdf_desk } from "../../js/ui/ui_pdf_desk.js";
import api from "../../js/ClientApi/api.js"
import {parseUrlParams, dialogConfirm, redirect, urlWatching, getPaths, msgError } from "../../js/ui/core.js"

var filesView = await View(import.meta, class FilesView extends BaseScope {
    listOfApp = [undefined]
    currentApp = undefined
    listOfFiles = []
    currentAppName = undefined
    hasSelected=false
    async init() {
        this.ui={
            hasSelected:false
        }
        var queryData = parseUrlParams();
        var r =await this.$getElement();
        $(window).resize(()=>{
                $(r).css({
                    "max-height":$(document).height()-100
                })
            })
            $(r).css({
                    "max-height":$(document).height()-100
                })


        this.listOfApp = await api.post(`admin/apps`, {
            
        })
        this.currentApp = this.listOfApp[0];
        this.currentAppName = this.currentApp.Name;
        await this.doLoadAllFiles();
        this.$applyAsync();
        debugger;
    }
    async doLoadAllFileByApp(appName) {
        this.listOfFiles = await api.post(`${appName}/files`, {
            
        });
        this.$applyAsync();
    }
    async showAddTagsButton(){
        for(var i=0;i<this.listOfFiles.length;i++){
            if(this.listOfFiles[i].isSelected){
                this.ui.hasSelected=true;
                this.$applyAsync();
                return;

            }
        }
        this.ui.hasSelected=false;
        this.$applyAsync();
    }
    async doAddTags(){
        this.showAddTags= true;
        this.$applyAsync();
    }
    async doLoadAllFiles() {
        var me = this;

        
        this.listOfFiles = await api.post(`${this.currentAppName}/files`, {
           
            PageIndex: 0,
            PageSize: 20,
            FieldSearch: "FileName",
            ValueSearch: me.fileNameSearchValue
        });
        this.$applyAsync();
    }
    async doSearchByFileName() {
        await this.doLoadAllFiles();
    }
    async doOpenInWindows(item) {
        var r = await import("../player/index.js");
        var player = await r.default();
        player.playByItem(item);
        player.asWindow();



    }
    async doShowWindowAddTags() {
        var r = await import("../tags-editor/index.js");
        var selectedId=[]
        for(var i=0;i<this.listOfFiles.length;i++){
            if(this.listOfFiles[i].isSelected){
                selectedId.push(this.listOfFiles[i].UploadId);

            }
        }
        var editor = await r.default();
        editor.setData(this.currentAppName, this,selectedId);
        editor.asWindow();
    }
    async doOpenUploadWindow() {
        debugger;
        var uploadForm = await (await import("../upload/index.js")).default();
        uploadForm.setApp(this.currentAppName);
        uploadForm.asWindow();
    }
    async doOpenUploadZipWindow() {
        var uploadZipForm = await (await import("../zip_upload/index.js")).default();
        uploadZipForm.setApp(this.currentAppName);
        uploadZipForm.asWindow();
    }
    async doDelete(item) {
        if (await dialogConfirm(this.$res("Do you want to delete this item?"))) {
            var reg = await api.post(`${this.currentAppName}/files/delete`, {
                UploadId: item.UploadId
            });
            var ele = await this.$findEle(`[file-id='${item.UploadId}']`);
            ele.remove();
        }
    }
    doLoadMore(sender) {

        api.post(`${sender.scope.currentAppName}/files`, {
            Token: window.token,
            PageIndex: sender.pageIndex,
            PageSize: sender.pageSize,
            FieldSearch: "FileName",
            ValueSearch: sender.scope.fileNameSearchValue
        }).then(r => {
            sender.done(r);
        });

    }
    async doShowDetail(item){
        debugger;
        var r = await import("../file-info/index.js");
        var viewer = await r.default();
        await viewer.loadDetailInfo(this.currentAppName,item.UploadId)
         var win =await viewer.asWindow();
         win.doMaximize()
         console.log(win);
    }
});
export default filesView;