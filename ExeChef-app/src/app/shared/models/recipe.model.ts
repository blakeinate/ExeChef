import {Profile }from './profile.model';
import {Ingredient}from './ingredient.model';

export class Recipe{
    _id:{ $oid:string };
    name : string;
    image_name: string;
    tags: Array<string> = [];
    steps : Array<string> = [];
    author : string;
    description : string;
    private : boolean;
    ingredients : Array<Ingredient> = [];
    created_date :{ $date:string };
    modified_date :{ $date:string };
    in_favorites: boolean;
    favorited_count:number;
    user: Profile;
}
