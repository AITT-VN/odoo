import { Component } from "@odoo/owl";
import { user } from "@web/core/user";

export class WidgetHour extends Component {
    setup() {
        this.getDateTime();
        this.updateHour = setInterval(() => {
            this.getDateTime();
            this.render();
        }, 1000);
    }

    getDateTime(){
        const lang = user.context.lang.replace("_", "-");
        this.currentTime = new Date().toLocaleTimeString();
        try {
            this.currentDate = new Date().toLocaleDateString(lang, {
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric"
            });
        }
        catch (e) {
            this.currentDate = new Date().toLocaleDateString();
        }
    }

    destroy(){
        clearInterval(this.updateHour);
    }
}

WidgetHour.template = "main_menu.WidgetHour";
