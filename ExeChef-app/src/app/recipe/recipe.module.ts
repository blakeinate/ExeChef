import { ModuleWithProviders, NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { RecipeComponent } from './recipe.component';
import { RecipeCommentComponent } from './recipe-comment.component';
import { RecipeResolver } from './recipe-resolver.service';
import { SharedModule } from '../shared';

const recipeRouting: ModuleWithProviders = RouterModule.forChild([
  {
    path: 'recipe/:recipe_id',
    component: RecipeComponent,
    resolve: {
      recipe: RecipeResolver
    }
  }
]);

@NgModule({
  imports: [
    recipeRouting,
    SharedModule
  ],
  declarations: [
    RecipeComponent,
    RecipeCommentComponent,
  ],

  providers: [
    RecipeResolver
  ]
})
export class RecipeModule {}
