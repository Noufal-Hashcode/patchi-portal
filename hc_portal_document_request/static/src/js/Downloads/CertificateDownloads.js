/** @odoo-module **/

import {useService, useBus, useEffect} from "@web/core/utils/hooks";
import {Mutex} from "@web/core/utils/concurrency";
import {Downloads} from "@odoo_custom_portal/js/Downloads/Downloads";
import {DownloadsPaySlipTable} from "@odoo_custom_portal/js/Downloads/Downloads";


const {Component} = owl;
import core from 'web.core';

const {useState, onWillStart, useExternalListener, useRef} = owl.hooks;



console.log("djhbjfbf11", Downloads, DownloadsPaySlipTable)
export class CertificateDownloads extends Component {


    setup() {
        this.rpcService = useService("rpc");
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.notificationService = useService("notification");

        this.state = useState({
            certificate_data: {},
            certificate_count: 0,
            current_page: 1,
            items_per_page: 10,
            all_selected: false,
            selected_items: []
        })

        this.loading = useState({
            is_loading: false,
        })


        useEffect(
            () => {
                this.loading.is_loading = true
                console.log("djdff")
                this.getDataUpdateState(this.state.current_page, this.state.items_per_page).then((data) => {
                    this.loading.is_loading = false
                    if (data.length > 0) {
                        this.state.certificate_data = data[0].payslips_data
                        this.state.certificate_count = data[0].payslips_count
                        this.state.selected_items = []
                    }
                })
            },
            () => [this.state.current_page]
        );
    }

    backButton = () => {
        // console.log(this.state.current_page)
        if (this.state.current_page > 1) {
            this.state.current_page -= 1
            this.state.all_selected = false
            this.state.selected_items = []
        }
    }
    nextButton = () => {
        if (this.state.certificate_count > this.state.items_per_page * this.state.current_page) {
            this.state.current_page += 1
            this.state.all_selected = false
            this.state.selected_items = []
        }
    }
    selectAllItems = () => {
        let selected_items = []

        console.log("1223", this)
        if (this.state.all_selected) {
        console.log("1223 rrrr")
            let certificate_data = this.state.certificate_data.map((line) => {
                return {...line, is_selected: false}
            })
            this.state.certificate_data = certificate_data
            this.state.all_selected = false
            this.state.selected_items = []
        } else if (!this.state.all_selected) {
        console.log("122         tttttt3",this.state)
            let certificate_data = this.state.certificate_data.map((line) => {
                selected_items.push(line.id)
                return {...line, is_selected: true}
            })
            console.log("popopodsds", selected_items, certificate_data)
            Object.assign(this.state, {
                certificate_data: certificate_data,
                all_selected: true,
                selected_items: selected_items
            })
        }

    }
    selectIndividualItem = (id) => {
        console.log(id)
        let clicked_index = []
        let is_all_selected = true
        let selected_items = []
        let certificate_data = this.state.certificate_data.map((line, index) => {
            if (line.id === id) {
                clicked_index.push(index)
                if (line.is_selected) {
                    this.state.selected_items.forEach((selected_item) => {
                        if (selected_item !== line.id) {
                            selected_items.push(selected_item)
                        }
                    })
                } else {
                    selected_items = [...this.state.selected_items, line.id]
                }

                return {...line, is_selected: !line.is_selected}
            } else {
                return line
            }
        })

        certificate_data.forEach((line)=>{
            if(is_all_selected){
                is_all_selected =line.is_selected
            }
        })



        console.log(clicked_index)
        if (clicked_index.length === 1) {
            this.state.certificate_data=certificate_data
            this.state.selected_items = selected_items
            this.state.all_selected = is_all_selected
            console.log(selected_items)
            console.log(is_all_selected)


        }

    }
    printReport = async () => {
        let url_list = '?list_ids='+ this.state.selected_items.toString();
                    this.actionService.doAction(
                {
                    type: 'ir.actions.act_url',
                    url:'/my/certificate/pdf/download' + url_list

                }
            )


    }

    getDataUpdateState = async (page_number, items_per_page) => {

        let data = await this.rpcService(`/hc_portal_document_request/certificate_data`, {
            page_number: page_number,
            items_per_page: items_per_page
        });
        console.log(data)
        return data
    }


}


//Downloads.template = "odoo_custom_portal.Downloads"
CertificateDownloads.template = "odoo_custom_portal.DownloadsCertificateTable"
Downloads.components = {
    DownloadsPaySlipTable,CertificateDownloads
}

