/** @odoo-module **/

console.log("xdcsjxhhdcs rrrrrrrr      x")
import {useService, useBus, useEffect} from "@web/core/utils/hooks";
import {Mutex} from "@web/core/utils/concurrency";

const {Component} = owl;
import core from 'web.core';
//import {MainPortal} from "@hc_portal_document_request/js/MainPortal/MainPortal";

const {useState, onWillStart, useExternalListener, useRef} = owl.hooks;

export class CertificateRequests extends Component {


    setup() {
    console.log("popopopo")
        this.rpcService = useService("rpc");
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.notificationService = useService("notification");

        this.state = useState({
            employee_data: {},
            employee_data_non_edited: {},
            current_page: 1,
            edit_enable: false,
            save_refresh_page: 1,

            error_display:false,
            error_msg:'Please check your inputs',
            successful_changes:false
        })

        this.loading = useState({
            is_loading: true,
        })
        console.log("skjhjhshhs111")


        useEffect(
            () => {
                this.loading.is_loading = true

                console.log("skjhjhshhs",Object, this.state)
                if (Object.keys(this.state.employee_data).length > 0) {

                    console.log("ashah hhhs")
                    this.saveData(this.state.employee_data).then(() => {
                        this.getDataUpdateState().then((data) => {
                            this.loading.is_loading = false
                            if (data.length > 0) {
                                this.state.employee_data = data[0].employee_data
                            }
                        })

                    }).catch((e) => {
                        // console.log(e)
                    })

                } else {

                    console.log("ashah hhhs11111")
                    this.getDataUpdateState().then((data) => {
                        console.log(data)
                        this.loading.is_loading = false
                        if (data.length > 0) {
                            this.state.employee_data = data[0].employee_data
                        }
                    })
                }
            },
            () => [this.state.save_refresh_page]
        );
    }

    changeTab = (page_number) => {
        this.state.current_page = page_number
    }
    // enablePopUp = (notice) => {
    //     this.state.error_display = true
    //
    // }
    disablePopUp = (notice) => {
        this.state.error_display = false
        this.state.successful_changes = false
        this.state.error_msg= 'Please check your inputs'

    }

    changeType = (e) => {
        let country_id = []
        this.state.employee_data.countries_ids.forEach((line) => {

                console.log("1country_id1")
            if (line[0] === parseInt(e.target.value)) {

            console.log("1222country_id1")
                country_id = line
            }
        })
        console.log("1country_idzzzz1", country_id)
        this.state.employee_data['certificate_type'] = country_id
        this.state.save_refresh_page += 1
    }
//    changeState = (e) => {
//        let state_id = []
//        this.state.employee_data.state_ids.forEach((line) => {
//            if (line[0] === parseInt(e.target.value)) {
//                state_id = line
//            }
//        })
//        this.state.employee_data.address_home_id.state_id = state_id
//    }
//    changeMaritalState = (e) => {
//        this.state.employee_data.gender = e.target.value
//    }
//    changeGender = (e) => {
//        this.state.employee_data.marital = e.target.value
//    }
//    changePassword = async () => {
//        let fields = {
//            old_password: this.state.old_password,
//            new_password: this.state.new_password,
//            confirm_password: this.state.confirm_password
//        }
//
//        let data = await this.rpcService(`/portal/web/session/change_password`, {fields: fields});
//        console.log(data)
//        if(data.new_password){
//            this.state.successful_changes =true
//
//
//        }else{
//            this.state.error_display =true
//            if(data.error){
//                this.state.error_msg = data.error
//            }
//
//        }
//    }

    clickOption = (e) => {
        // console.log(e)
    }
    editButton = () => {
        this.state.edit_enable = true

    }

    createButton = () => {
        console.log("pppppppppppppppppddddddddddddddd", this, )
//        this.state.edit_enable = true
            this.state.save_refresh_page
            this.setup()

    }

    discardChanges = () => {
        this.loading.is_loading = true
        this.getDataUpdateState().then((data) => {
            this.loading.is_loading = false
            if (data.length > 0) {
                this.state.employee_data = data[0].employee_data
            }
        })
        this.state.edit_enable = false

    }
    saveChanges = () => {
        this.state.save_refresh_page += 1
        this.state.edit_enable = false
        this.state.current_page = 2

    }

    onChangeField = (e, field) => {
         console.log("re", e,field)

        let value = e.target.value
         console.log("ree", value)
        if (field === 'address') {
            this.state.employee_data['addressee'] = value
        } else if (field === 'travel') {
            this.state.employee_data['travel'] = value
//        } else if (field === 'request_date') {
//            this.state.employee_data['request_date'] = value
        } else if (field === 'issued_to') {
            this.state.employee_data['issued_to'] = value
        }

    }

    getDataUpdateState = async () => {
        let data = await this.rpcService(`/hc_portal_document_request/certificate_request`, {
            page_number: 1,
            items_per_page: 10
        });
        // console.log(data)
        return data
    }

    saveData = async (employee_data) => {
        let saving_data = {}
        if (Object.keys(employee_data).length > 0) {
            saving_data = {
                emp_id: employee_data.id,
                req_date: employee_data.request_date,
                addressee: employee_data.addressee,
                travel: employee_data.travel,
                issued_to: employee_data.issued_to,

                certificate_type: employee_data.certificate_type ? employee_data.certificate_type[0] : false,

            }
        }
        // console.log(saving_data)

        let data = await this.rpcService(`/hc_portal_document_request/certificate_request/save-data`, {
            saving_data: saving_data,
        });
        // console.log(data)
        return data
    }


}


CertificateRequests.template = "hc_portal_document_request.CertificateRequests"


