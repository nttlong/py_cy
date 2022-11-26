import { BaseScope, View } from "./../../js/ui/BaseScope.js";
//import { ui_rect_picker } from "../../js/ui/ui_rect_picker.js";
//import { ui_pdf_desk } from "../../js/ui/ui_pdf_desk.js";
import api from "../../js/ClientApi/api.js"
import { redirect, urlWatching, getPaths, msgError } from "../../js/ui/core.js"

var searchView = await View(import.meta, class SearchView extends BaseScope {
    listOfApp = [1]
    currentApp = undefined
    listOfFiles = []
    highlight=false
    currentAppName = undefined
    async init() {
        var mainEle = await this.$getElement();
        $(window).resize(()=>{
                $(mainEle).css({
                    "max-height":$(document).height()-100
                })
            })
            $(mainEle).css({
                    "max-height":$(document).height()-100
               })
        this.listOfApp = await api.post(`admin/apps`, {
            Token: window.token
        })
        this.currentApp = this.listOfApp[0];
        this.currentAppName = this.currentApp.Name;
        
        this.$apply();
    }
    async doFullTextSearch() {
       if(this.highlight){
            this.data = await api.post(`${this.currentAppName}/search`, {
                content: this.searchContent,
                page_size:20,
                page_index:0,
                highlight:this.highlight
            });
            this.$applyAsync();
        }
        else {
            this.data = await api.post(`${this.currentAppName}/search`, {
                content: this.searchContent,
                page_size:1000,
                page_index:0
            });
            this.$applyAsync();
        }
    }
    
    
    
    
    
   
});
export default searchView;