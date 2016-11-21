import {Component, OnInit} from "@angular/core";
import {Observable, Operator} from "rxjs";

@Component({
    selector: 'peek-client-home',
    templateUrl: 'home.component.html',
    styleUrls: ['home.component.css']
})
export class HomeComponent implements OnInit {
    data = ["thiss"];
    service: Observable<string>;
    observerIn;

    constructor() {

    }

    ngOnInit() {
        let self = this;
        this.service = Observable.create(function(observer){
            self.observerIn = observer;
        });

        this.service
            .subscribe(val => self.addData(val));

        self.go();

    }

    addData(s:string) {
        console.log(s);
        this.data.push(s);
    }

    go() {
        let self = this;
        setTimeout(function () {
            self.observerIn.next(`new ${self.data.length}`);
            self.go();
        }, 2000);
    }

}
