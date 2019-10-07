{
  network.description = "Web server";

  lb_common =
   
    { config, pkgs, resources, ... }:
    {
      imports = [
        <lbdevops/nixos/logicblox/lb40-module.nix>
      ];
      services.logicblox.enable = true;
      services.logicblox.logicblox = /nix/store/mpwz3cylc8w24i7dcf4hr0qwf7g5b275-logicblox-4.13.0-207bc1c6cf29d3f6ea3a685a8c32a4144bcc5e42;
      deployment.targetEnv = "virtualbox";
      deployment.virtualbox.memorySize = 4096; # megabytes
      deployment.virtualbox.vcpu = 2; # number of cpus
      deployment.virtualbox.headless = true;
      services.logicblox.config.lb-web-client="[Headers]\nAuthorization=${resources.saasAuths.saasAuth.token}"; 
      networking.firewall.allowedTCPPorts = [ 8080 55183 ];
    };
    resources.saasAuths.saasAuth = { lib, ... }:
      { 
         name = "lbgenesis";
         account = "gpm";
         account_token_path = "/tmp/gpm_account_token";
         url = "http://localhost:55183/generate-token";
      };
}
