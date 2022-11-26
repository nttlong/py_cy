import rcmpactModule from "./rcmpt.js"

rcmpactModule.directive("rcmpctGrid", [() => {
    return {
        restrict: "E",
        replace: true,
        transclude: true,
        template: `<div ng-transclude></div>`,
        link: (s, e, a) => {
            $(e[0]).hide();
            /**
             * display: grid;
  grid-template-columns: 80px 200px auto 40px;
             * */
            if (!a.cols)
                return;
            var colsInfo = a.cols.split(')(');
            var colsInfoPars = {}
            var wathTimeInterVal = -1;
            async function watchCosInfo(ele, _cols, acysnCallback) {
                var oldW = $(e.parents()[0]).innerWidth();
                async function run() {
                    if ($(e.parents()[0]).innerWidth() != oldW) {
                        oldW = $(e.parents()[0]).innerWidth()
                        await acysnCallback(oldW)
                    }
                    wathTimeInterVal = setTimeout(run, 500);

                }

                await run();
            }
            s.$on("$destroy", () => {
                clearInterval(wathTimeInterVal);
            });
            if (colsInfo.length == 1) {
                $(e[0]).css({
                    display: "grid",

                    "grid-template-columns": a.cols
                });
                $(e[0]).show();
            }
            else if (colsInfo.length > 1) {
                var colsConfig = []
                colsInfo.forEach((item, index) => {
                    item = item.replace('(', '').replace(')', '');
                    var arr = item.split(',')
                    var dataItem = {
                        from: arr[0] == '' ? 0 : parseInt(arr[0]),
                        to: arr[1] == '' ? 10000000 : parseInt(arr[1]),
                        cols: arr[2]
                    }
                    colsConfig.push(dataItem)
                });
                watchCosInfo(e, colsConfig, async (w) => {
                    var retCol = colsConfig[0].cols;
                    for (var i = 0; i < colsConfig.length; i++) {
                        if (w >= colsConfig[i].from && w < colsConfig[i].to) {
                            retCol = colsConfig[i];
                           

                        }
                    }
                    $($(e[0]).parents()[0]).css({
                        display: "grid",

                        "grid-template-columns": retCol.cols
                    })
                    $(e[0]).show();
                    
                }).then()
            }
            class component {


            }
            a.$observe("resouce", (v) => {
                alert(v);
            });

        }
    }
}]);


export { rcmpactModule }