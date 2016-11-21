import { PeekClientPage } from './app.po';

describe('peek-client App', function() {
  let page: PeekClientPage;

  beforeEach(() => {
    page = new PeekClientPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
