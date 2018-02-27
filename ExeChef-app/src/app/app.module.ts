import { BrowserModule } from '@angular/platform-browser';
import { NgModule, ModuleWithProviders } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HomeModule } from './home/home.module';
import {AuthModule} from "./auth/auth.module";
import { AppComponent } from './app.component';

import {
  FooterComponent,
  HeaderComponent,
} from './shared';

const rootRouting: ModuleWithProviders = RouterModule.forRoot([], { useHash: true });

@NgModule({
  declarations: [
    AppComponent,
    FooterComponent,
    HeaderComponent
  ],
  imports: [
    BrowserModule,
    AuthModule,
    HomeModule,
    rootRouting,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
