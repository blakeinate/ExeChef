import { BrowserModule } from '@angular/platform-browser';
import { NgModule, ModuleWithProviders } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HomeModule } from './home/home.module';
import { ProfileModule } from './profile/profile.module';
import {AuthModule} from "./auth/auth.module";
import { AppComponent } from './app.component';
import { SettingsModule}from './settings/settings.module';
import {
  ApiService,
  AuthGuard,
  UserService,
  JwtService,
  ProfilesService,
  FooterComponent,
  HeaderComponent,
  SharedModule,
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
    ProfileModule,
    rootRouting,
    SharedModule,
    SettingsModule,
  ],
  providers: [
    ApiService,
    AuthGuard,
    UserService,
    JwtService,
    ProfilesService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
