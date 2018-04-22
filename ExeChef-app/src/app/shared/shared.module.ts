import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { RouterModule } from '@angular/router';
import { RecipeMetaComponent } from './recipe-helpers';
import { FavoriteButtonComponent, FollowButtonComponent } from './buttons';

import {ListErrorsComponent} from './errorList';
import {ShowAuthedDirective} from './show-authed.directive';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    RouterModule
  ],
  declarations: [
    RecipeMetaComponent,
    FavoriteButtonComponent,
    FollowButtonComponent,
    ListErrorsComponent,
    ShowAuthedDirective
  ],
  exports: [
    RecipeMetaComponent,
    CommonModule,
    FavoriteButtonComponent,
    FollowButtonComponent,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    ListErrorsComponent,
    RouterModule,
    ShowAuthedDirective
  ]
})
export class SharedModule {}
