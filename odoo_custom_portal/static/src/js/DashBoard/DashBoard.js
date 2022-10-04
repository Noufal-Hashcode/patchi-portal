/** @odoo-module **/

import {useService, useBus, useEffect} from "@web/core/utils/hooks";
import {Mutex} from "@web/core/utils/concurrency";
import {useAssets} from "@web/core/assets";

const {Component} = owl;
import core from 'web.core';

const {useState, onWillStart, useExternalListener, useRef, onPatched, onMounted} = owl.hooks;

export class DashBoard extends Component {


    setup() {
        this.rpcService = useService("rpc");
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.notificationService = useService("notification");

        this.state = useState({
            employee_data: {},
            attendances_data: [],
            leave_balances_data: [],
            leave_requests_data:[]
        })

        this.loading = useState({
            is_loading: false,
        })
        this.barcode_line = useRef('shift_chart')
        this.canvasRef = useRef("canvas");
        this.containerRef = useRef("container");
        useAssets({jsLibs: ["/odoo_custom_portal/static/src/lib/frappe-gantt/frappe-gantt.js",]});

        useEffect(
            () => {
                this.loading.is_loading = true
                this.getDataUpdateState().then((data) => {
                    this.loading.is_loading = false
                    if (data.length > 0) {
                        this.state.employee_data = data[0].employee_data
                        this.state.attendances_data = data[0].attendances_data
                        this.state.leave_balances_data = data[0].leave_balances_data
                        this.state.leave_requests_data =data[0].leave_requests_data
                    }
                })
            },
            () => []
        );
        useEffect(
            () => {

                let tasks = [
                    {
                        id: 'Task 1',
                        name: 'Buy hosting',
                        start: '2022-01-22',
                        end: '2022-01-23',
                        progress: 100,
                    },
                     {
                        id: 'Task 1',
                        name: 'Buy hosting',
                        start: '2022-01-25',
                        end: '2022-01-26',
                        progress: 100,
                    },
                ]
                let ganttChart = new Gantt(".gantt-selector", tasks, {});



            });
    }

    getDataUpdateState = async (part_id) => {

        let data = await this.rpcService(`/odoo_custom_portal/dashboard_data`);
        console.log(data)
        return data
    }

    mounted() {

    }


}


DashBoard.template = "odoo_custom_portal.DashBoard"

// function debugOwl(t,e){let n,o="[OWL_DEBUG]";function r(t){let e;try{e=JSON.stringify(t||{})}catch(t){e="<JSON error>"}return e.length>200&&(e=e.slice(0,200)+"..."),e}if(Object.defineProperty(t.Component,"current",{get:()=>n,set(s){n=s;const i=s.constructor.name;if(e.componentBlackList&&e.componentBlackList.test(i))return;if(e.componentWhiteList&&!e.componentWhiteList.test(i))return;let l;Object.defineProperty(n,"__owl__",{get:()=>l,set(n){!function(n,s,i){let l=`${s}<id=${i}>`,c=t=>console.log(`${o} ${l} ${t}`),u=t=>(!e.methodBlackList||!e.methodBlackList.includes(t))&&!(e.methodWhiteList&&!e.methodWhiteList.includes(t));u("constructor")&&c(`constructor, props=${r(n.props)}`);u("willStart")&&t.hooks.onWillStart(()=>{c("willStart")});u("mounted")&&t.hooks.onMounted(()=>{c("mounted")});u("willUpdateProps")&&t.hooks.onWillUpdateProps(t=>{c(`willUpdateProps, nextprops=${r(t)}`)});u("willPatch")&&t.hooks.onWillPatch(()=>{c("willPatch")});u("patched")&&t.hooks.onPatched(()=>{c("patched")});u("willUnmount")&&t.hooks.onWillUnmount(()=>{c("willUnmount")});const d=n.__render.bind(n);n.__render=function(...t){c("rendering template"),d(...t)};const h=n.render.bind(n);n.render=function(...t){const e=n.__owl__;let o="render";return e.isMounted||e.currentFiber||(o+=" (warning: component is not mounted, this render has no effect)"),c(o),h(...t)};const p=n.mount.bind(n);n.mount=function(...t){return c("mount"),p(...t)}}(s,i,(l=n).id)}})}}),e.logScheduler){let e=t.Component.scheduler.start,n=t.Component.scheduler.stop;t.Component.scheduler.start=function(){this.isRunning||console.log(`${o} scheduler: start running tasks queue`),e.call(this)},t.Component.scheduler.stop=function(){this.isRunning&&console.log(`${o} scheduler: stop running tasks queue`),n.call(this)}}if(e.logStore){let e=t.Store.prototype.dispatch;t.Store.prototype.dispatch=function(t,...n){return console.log(`${o} store: action '${t}' dispatched. Payload: '${r(n)}'`),e.call(this,t,...n)}}}
// debugOwl(owl, {
//   // componentBlackList: /App/,  // regexp
//   // componentWhiteList: /SomeComponent/, // regexp
//   // methodBlackList: ["mounted"], // list of method names
//   // methodWhiteList: ["willStart"], // list of method names
//   logScheduler: false,  // display/mute scheduler logs
//   logStore: true,     // display/mute store logs
// });
//
