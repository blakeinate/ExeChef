import { ModuleWithProviders, NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { ProfileRecipesComponent } from './profile-recipes.component';
import { ProfileComponent } from './profile.component';
import { ProfileResolver } from './profile-resolver.service';
import { SharedModule } from '../shared';

const profileRouting: ModuleWithProviders = RouterModule.forChild([
  {
    path: 'profile/:username',
    component: ProfileComponent,
    resolve: {
      profile: ProfileResolver
    },
    children: [
      {
        path: 'created',
        component: ProfileRecipesComponent
      },
      {
        path: 'favorites',
        component: ProfileRecipesComponent
      }
    ]
  }
]);

@NgModule({
  imports: [
    profileRouting,
    SharedModule
  ],
  declarations: [
    ProfileComponent,
    ProfileRecipesComponent
  ],

  providers: [
    ProfileResolver
  ]
})
export class ProfileModule {}
