import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';

import { Recipe } from '../models';
import { RecipesService, UserService } from '../services';

@Component({
  selector: 'favorite-button',
  templateUrl: './favorite-button.component.html'
})
export class FavoriteButtonComponent {
  constructor(
    private recipesService: RecipesService,
    private router: Router,
    private userService: UserService
  ) {}

  @Input() recipe: Recipe;
  @Output() onToggle = new EventEmitter<boolean>();
  isSubmitting = false;

  toggleFavorite() {
    this.isSubmitting = true;

    this.userService.isAuthenticated.subscribe(
      (authenticated) => {
        // Not authenticated? Push to login screen
        if (!authenticated) {
          this.router.navigateByUrl('/login');
          return;
        }

        this.recipesService.toggleFavorite(this.recipe._id.$oid)
        .subscribe(
          data => {
            this.isSubmitting = false;
            this.onToggle.emit(data["emit"]);
          },
          err => this.isSubmitting = false
        );

      }
    )


  }

}
