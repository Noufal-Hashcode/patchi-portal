/** @odoo-module **/

import {useService, useBus, useEffect} from "@web/core/utils/hooks";
import {Mutex} from "@web/core/utils/concurrency";
const {Component} = owl;
import core from 'web.core';
const {useState, onWillStart, useExternalListener, useRef} = owl.hooks;

import { MainPortal } from "@odoo_custom_portal/js/MainPortal/MainPortal";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";

import {DashBoard} from "@odoo_custom_portal/js/DashBoard/DashBoard";
import {Newsletter} from "@odoo_custom_portal/js/Newsletter/Newsletter";
import {Alerts} from "@odoo_custom_portal/js/Alerts/Alerts";
import {MyProfile} from "@odoo_custom_portal/js/MyProfile/MyProfile";
import {Downloads} from "@odoo_custom_portal/js/Downloads/Downloads";
import {MyShifts} from "@odoo_custom_portal/js/MyShifts/MyShifts";
import {Requests} from "@odoo_custom_portal/js/Requests/Requests";

import {CertificateRequests} from "@hc_portal_document_request/js/CertificateRequests/CertificateRequests";

console.log("MainPortal", MainPortal)
patch(MainPortal.prototype, "@hc_portal_document_request/js/MainPortal/MainPortal", {

        setup() {
        this.rpcService = useService("rpc");
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.notificationService = useService("notification");

        this.main_menu = useState({
            is_main_dashboard_visible: true,
            is_my_profile_visible: false,
            is_my_shifts_visible: false,
            is_requests_visible: false,
            is_alerts_visible: false,
            is_downloads_visible: false,
            is_newsletter_visible: false,
            is_certificate_request_visible: false,
            active: false,
            sidebar_clicked: 0
            // is_small_logo:false,
            // is_ready_to_load:false
        })
        // this.sidebar_state = useState({

            // is_small_logo:false,
            // is_ready_to_load:false
        // })
        // this.sidebar = useRef('sidebar')
        // console.log(this.sidebar)
        // useEffect(
        //     () => {
        //         console.log(this.sidebar.el.offsetWidth)
        //         if(this.sidebar.el.offsetWidth > 55 && this.sidebar.el.offsetWidth <65){
        //             this.main_menu.is_small_logo = true
        //             this.main_menu.is_ready_to_load = true
        //         }
        //     },
        //     () => [this.sidebar.el.offsetWidth,this.main_menu.active]
        // );

        useEffect(
            () => {
                console.log(window.innerWidth)
                if (window.innerWidth > 1240){
                    // if(this.main_menu.active){
                    //     this.main_menu.active = false
                    // }

                }else if(window.innerWidth < 1240){
                    if(this.main_menu.active){
                        this.main_menu.active = false
                    }
                }
                // console.log(this.sidebar.el.offsetWidth)
                // if(this.sidebar.el.offsetWidth > 55 && this.sidebar.el.offsetWidth <65){
                //     this.main_menu.is_small_logo = true
                //     this.main_menu.is_ready_to_load = true
                // }
            },
            () => [this.main_menu.sidebar_clicked]
        );
    },


    onClickMainMenuItemRe(menu_name) {

//        this.main_menu.sidebar_clicked +=1
//
//        let new_state = {
//            is_main_dashboard_visible: false,
//            is_my_profile_visible: false,
//            is_requests_visible: false,
//            is_my_shifts_visible: false,
//            is_alerts_visible: false,
//            is_downloads_visible: false,
//            is_newsletter_visible: false,
//            is_certificate_request_visible: false,
//        }
//        if (menu_name === 'certificate_request') {
//            new_state.is_certificate_request_visible = true
//        }
//        Object.assign(this.main_menu, new_state)
//
//        console.log("sdjsad", this)


                this.main_menu.sidebar_clicked +=1

        let new_state = {
            is_main_dashboard_visible: false,
            is_my_profile_visible: false,
            is_requests_visible: false,
            is_my_shifts_visible: false,
            is_alerts_visible: false,
            is_downloads_visible: false,
            is_newsletter_visible: false,
            is_certificate_request_visible: false,
        }
        if (menu_name === 'main_dashboard') {
            new_state.is_main_dashboard_visible = true
        } else if (menu_name === 'my_profile') {
            new_state.is_my_profile_visible = true
        } else if (menu_name === 'requests') {
            new_state.is_requests_visible = true
        } else if (menu_name === 'my_shifts') {
            new_state.is_my_shifts_visible = true
        } else if (menu_name === 'alerts') {
            new_state.is_alerts_visible = true
        } else if (menu_name === 'downloads') {
            new_state.is_downloads_visible = true
        } else if (menu_name === 'newsletter') {
            new_state.is_newsletter_visible = true
        } else if (menu_name === 'certificate_request') {
            new_state.is_certificate_request_visible = true
        }
        Object.assign(this.main_menu, new_state)

    },



});



MainPortal.components = {DashBoard, MyProfile, MyShifts, Alerts, Downloads, Newsletter, Requests, CertificateRequests}
