import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import {
  Recipe,
  RecipesService,
  Comment,
  CommentsService,
  User,
  UserService
} from '../shared';

@Component({
  selector: 'Recipe-page',
  templateUrl: './Recipe.component.html'
})
export class RecipeComponent implements OnInit {
  recipe: Recipe;
  currentUser: User;
  canModify: boolean;
  comments: Comment[];
  commentControl = new FormControl();
  commentFormErrors = {};
  isSubmitting = false;
  isDeleting = false;

  constructor(
    private route: ActivatedRoute,
    private RecipesService: RecipesService,
    private commentsService: CommentsService,
    private router: Router,
    private userService: UserService,
  ) { }

  ngOnInit() {
    // Retreive the prefetched Recipe
    this.route.data.subscribe(
      (data: { recipe: Recipe }) => {
        this.recipe = data.recipe;
        this.populateComments();
      }
    );

    // Load the current user's data
    this.userService.currentUser.subscribe(
      (userData: User) => {
        this.currentUser = userData;
        this.canModify = (this.currentUser.username === this.recipe.author);
      }
    );
  }

  onToggleFavorite(favorited: boolean) {
    this.recipe.in_favorites = favorited;
    if (favorited) {
      this.recipe.favorited_count++;
    } else {
      this.recipe.favorited_count--;
    }
  }

  onToggleFollowing(following: boolean) {
    this.recipe.user.am_i_following = following;
  }

  deleteRecipe() {
    this.isDeleting = true;
    this.RecipesService.destroy(this.recipe._id.$oid)
      .subscribe(
        success => {
          this.router.navigateByUrl('/');
        }
      );
  }


    populateComments() {
    this.commentsService.getAll(this.recipe._id.$oid)
      .subscribe(comments => this.comments = comments);
  }

  addComment() {
    this.isSubmitting = true;
    this.commentFormErrors = {};

    let commentBody = this.commentControl.value;
    this.commentsService
      .add(this.recipe._id.$oid, commentBody)
      .subscribe(
        comment => {
          this.comments.unshift(comment);
          this.commentControl.reset('');
          this.isSubmitting = false;
        },
        errors => {
          this.isSubmitting = false;
          this.commentFormErrors = errors;
        }
      );
  }

  onDeleteComment(comment) {
    //console.log("the ID for comment",comment._id.$oid);
    this.commentsService.destroy(comment._id.$oid)
      .subscribe(
        success => {
          console.log("not reaching");
          this.comments = this.comments.filter((item) => item !== comment);
        }
      );
  }
}
