import {BrowserModule} from "@angular/platform-browser";
import {NgModule} from "@angular/core";
import {FormsModule} from "@angular/forms";
import {HttpModule} from "@angular/http";
import {HomeComponent} from "../home/home.component";
import {RootComponent} from "./root.component";
import { AlertModule } from 'ng2-bootstrap';


@NgModule({
    declarations: [
        RootComponent,
        HomeComponent,
    ],
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        AlertModule
    ],
    providers: [],
    bootstrap: [RootComponent]
})
export class RootModule {
}
