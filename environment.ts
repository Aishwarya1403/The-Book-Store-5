export const environment = {
    production: false,
    apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
    auth0: {
      url: 'dev-b9uuiwyh.us', // the auth0 domain prefix
      audience: 'https://bookshop/', // the audience set for the auth0 app
      clientId: 'qO41R3dBsVA4jrIng9cEaZmIocd4IHcF', // the client id generated for the auth0 app
      callbackURL: 'https://127.0.0.1:5000', // the base url of the running ionic application. 
    }
  };
  