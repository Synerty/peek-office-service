import "./vendor.ts";

import "./polyfills.ts";

import {platformBrowserDynamic} from "@angular/platform-browser-dynamic";
import {enableProdMode} from "@angular/core";
import {environment} from "./environments/environment";
import {RootModule} from "./peek_client/ui/root/root.module";


if (environment.production) {
    enableProdMode();
}

platformBrowserDynamic().bootstrapModule(RootModule);
