import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { RouterModule } from '@angular/router';
import {FollowButtonComponent} from "./buttons";
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
    FollowButtonComponent,
    ListErrorsComponent,
    ShowAuthedDirective
  ],
  exports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    FollowButtonComponent,
    ListErrorsComponent,
    RouterModule,
    ShowAuthedDirective
  ]
})
export class SharedModule {}
