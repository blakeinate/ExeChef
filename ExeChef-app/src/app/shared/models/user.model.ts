export class User{
  _id:{ $oid:string };
  username: string;
  password: string;
  email: string;
  favorites: string[];
  created: string[];
  followers: string[];
  following: string [];
  am_i_following: boolean;
  access_token: string;
  refresh_token: string;
}
