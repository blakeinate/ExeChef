import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { ApiService } from './api.service';
import { Comment } from '../models';


@Injectable()
export class CommentsService {
  constructor (
    private apiService: ApiService
  ) {}

  add(recipe_id, payload): Observable<Comment> {
    return this.apiService.post(`/Recipe/${recipe_id}/comments`, { comment: { body: payload } })
     .map(data => data.comment);
  }

  getAll(recipe_id): Observable<Comment[]> {
    return this.apiService.get(`/Recipe/${recipe_id}/comments`)
     .map(data => data.comments);
  }

  destroy(comment_id, recipe_id) {
    return this.apiService.delete(`/Recipe/${recipe_id}/comments/${comment_id}`);
  }

}
