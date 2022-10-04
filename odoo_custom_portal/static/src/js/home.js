/** @odoo-module **/

import concurrency from 'web.concurrency';
import publicWidget from 'web.public.widget';

import {qweb} from 'web.core';
import {Markup} from 'web.utils';

publicWidget.registry.HomePagePortal = publicWidget.Widget.extend({
    selector: '.home-wrapper',
    // xmlDependencies: ['/website/static/src/snippets/s_searchbar/000.xml'],
    events: {
        "click .sidebar-button": "_onSubmit",
    },


    /**
     * @constructor
     */
    init: function () {
        console.log('hello cunt')
        // this._super.apply(this, arguments);
        console.log('hello cunt')
    },
    /**
     * @override
     */
    start: function () {
        console.log('hello cunt')
        this.hamburger = this.$('.gantt-container-1');
        console.log(this.hamburger)
        //
        // this.searchType = this.$input.data('searchType');
        // this.order = this.$('.o_search_order_by').val();
        // this.limit = parseInt(this.$input.data('limit'));
        // this.displayDescription = this.$input.data('displayDescription');
        // this.displayExtraLink = this.$input.data('displayExtraLink');
        // this.displayDetail = this.$input.data('displayDetail');
        // this.displayImage = this.$input.data('displayImage');
        // this.wasEmpty = !this.$input.val();
        // // Make it easy for customization to disable fuzzy matching on specific searchboxes
        // this.allowFuzzy = !this.$input.data('noFuzzy');
        // if (this.limit) {
        //     this.$input.attr('autocomplete', 'off');
        // }
        //
        // this.options = {
        //     'displayImage': this.displayImage,
        //     'displayDescription': this.displayDescription,
        //     'displayExtraLink': this.displayExtraLink,
        //     'displayDetail': this.displayDetail,
        //     'allowFuzzy': this.allowFuzzy,
        // };

        // return this._super.apply(this, arguments);
    },
    //
    // //--------------------------------------------------------------------------
    // // Private
    // //--------------------------------------------------------------------------
    //
    // /**
    //  * @private
    //  */
    // async _fetch() {
    //     const res = await this._rpc({
    //         route: '/website/snippet/autocomplete',
    //         params: {
    //             'search_type': this.searchType,
    //             'term': this.$input.val(),
    //             'order': this.order,
    //             'limit': this.limit,
    //             'max_nb_chars': Math.round(Math.max(this.autocompleteMinWidth, parseInt(this.$el.width())) * 0.22),
    //             'options': this.options,
    //         },
    //     });
    //     const fieldNames = [
    //         'name',
    //         'description',
    //         'extra_link',
    //         'detail',
    //         'detail_strike',
    //         'detail_extra',
    //     ];
    //     res.results.forEach(record => {
    //         for (const fieldName of fieldNames) {
    //             if (record[fieldName]) {
    //                 if (typeof record[fieldName] === "object") {
    //                     for (const fieldKey of Object.keys(record[fieldName])) {
    //                         record[fieldName][fieldKey] = Markup(record[fieldName][fieldKey]);
    //                     }
    //                 } else {
    //                     record[fieldName] = Markup(record[fieldName]);
    //                 }
    //             }
    //         }
    //     });
    //     return res;
    // },
    // /**
    //  * @private
    //  */
    // _render: function (res) {
    //     const $prevMenu = this.$menu;
    //     this.$el.toggleClass('dropdown show', !!res);
    //     if (res && this.limit) {
    //         const results = res['results'];
    //         let template = 'website.s_searchbar.autocomplete';
    //         const candidate = template + '.' + this.searchType;
    //         if (qweb.has_template(candidate)) {
    //             template = candidate;
    //         }
    //         this.$menu = $(qweb.render(template, {
    //             results: results,
    //             parts: res['parts'],
    //             hasMoreResults: results.length < res['results_count'],
    //             search: this.$input.val(),
    //             fuzzySearch: res['fuzzy_search'],
    //             widget: this,
    //         }));
    //         this.$menu.css('min-width', this.autocompleteMinWidth);
    //         this.$el.append(this.$menu);
    //         this.$el.find('button.extra_link').on('click', function (event) {
    //             event.preventDefault();
    //             window.location.href = event.currentTarget.dataset['target'];
    //         });
    //         this.$el.find('.s_searchbar_fuzzy_submit').on('click', (event) => {
    //             event.preventDefault();
    //             this.$input.val(res['fuzzy_search']);
    //             const form = this.$('.o_search_order_by').parents('form');
    //             form.submit();
    //         });
    //     }
    //     if ($prevMenu) {
    //         $prevMenu.remove();
    //     }
    // },
    //
    // //--------------------------------------------------------------------------
    // // Handlers
    // //--------------------------------------------------------------------------
    //
    // /**
    //  * @private
    //  */
    // _onInput: function () {
    //     if (!this.limit) {
    //         return;
    //     }
    //     if (this.searchType === 'all' && !this.$input.val().trim().length) {
    //         this._render();
    //     } else {
    //         this._dp.add(this._fetch()).then(this._render.bind(this));
    //     }
    // },
    // /**
    //  * @private
    //  */
    // _onFocusOut: function () {
    //     if (!this.$el.has(document.activeElement).length) {
    //         this._render();
    //     }
    // },
    // /**
    //  * @private
    //  */
    // _onKeydown: function (ev) {
    //     switch (ev.which) {
    //         case $.ui.keyCode.ESCAPE:
    //             this._render();
    //             break;
    //         case $.ui.keyCode.UP:
    //         case $.ui.keyCode.DOWN:
    //             ev.preventDefault();
    //             if (this.$menu) {
    //                 let $element = ev.which === $.ui.keyCode.UP ? this.$menu.children().last() : this.$menu.children().first();
    //                 $element.focus();
    //             }
    //             break;
    //         case $.ui.keyCode.ENTER:
    //             this.limit = 0; // prevent autocomplete
    //             break;
    //     }
    // },
    /**
     * @private
     */
    _onSubmit: function (ev) {
        // if (this.$input[0].value) { // actual search
        //     this.limit = 0; // prevent autocomplete
        // } else { // clear button clicked
        //     this._render(); // remove existing suggestions
        //     ev.preventDefault();
        //     if (!this.wasEmpty) {
        //         this.limit = 0; // prevent autocomplete
        //         const form = this.$('.o_search_order_by').parents('form');
        //         form.submit();
        //     }
        // }
        console.log(ev)
        console.log(this.hamburger)
        // if (this.$('.sidebar').hasClass("active")) {
        //     this.$('.sidebar').removeClass('active')
        //     if(this.$('.user-icon').hasClass('to-small')){
        //            this.$('.user-icon').removeClass('to-small')
        //     }
        // }else{
        //     this.$('.sidebar').addClass('active')
        //     if(!this.$('.user-icon').hasClass('to-small')){
        //            this.$('.user-icon').addClass('to-small')
        //     }else{
        //
        //     }
        // }
        // this.
    },
});

export default {
    HomePagePortal: publicWidget.registry.HomePagePortal,
};
