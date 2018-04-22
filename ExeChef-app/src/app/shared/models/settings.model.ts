export class Settings{
  //username: string;
  bio?:string;
  email?: string;
  old_password?: string;
  new_password?: string;
  favorited_count?:number;
  favorites?: Array<string> = [];
  followers?: Array<string> = [];
  following?: Array<string> = [];
  am_i_following?: boolean;
  in_favorites?: boolean;
}
