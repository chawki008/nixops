{ config, lib, uuid, name, ... }:

with lib;

{

  options = {

    name = mkOption {
      default = "${name}-auth";
      type = types.str;
      description = "SAAS name";
    };
    
    account = mkOption {
      default = "logicblox-dev";
      type = types.str;
      description = "account";
    };
    
    url = mkOption {
      default = "";
      type = types.str;
      description = "SAAS url that Nixops is going to use to generate the user token from the account token, Nixops will pass the account token in the header and the deployment name as a query param name 'username'";
    };

    account_token_path = mkOption {
      default = "";
      type = types.str;
      description = "File that contains the saas account token, Nixops will read this file";
    };

    token = mkOption {
      default = "";
      type = types.str;
      description = "The user token, Nixops will get it from the saas url";
    };

  };
  config._type = "saasAuths";
}
