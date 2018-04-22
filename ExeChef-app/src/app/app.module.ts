import { BrowserModule } from '@angular/platform-browser';
import { NgModule, ModuleWithProviders } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HomeModule } from './home/home.module';
import { ProfileModule } from './profile/profile.module';
import {RecipeModule} from './recipe/recipe.module';
import {EditorModule} from './editor/editor.module';
import {AuthModule} from "./auth/auth.module";
import { AppComponent } from './app.component';
import { SettingsModule}from './settings/settings.module';
import {
  ApiService,
  AuthGuard,
  RecipesService,
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
    EditorModule,
    HomeModule,
    ProfileModule,
    RecipeModule,
    rootRouting,
    SharedModule,
    SettingsModule,
  ],
  providers: [
    ApiService,
    RecipesService,
    AuthGuard,
    UserService,
    JwtService,
    ProfilesService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
