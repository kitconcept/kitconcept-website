context('Nav Title tests suite', () => {
  describe('Nav Title tests', () => {
    beforeEach(() => {
      cy.intercept('GET', `/**/*?expand*`).as('content');
      cy.intercept('GET', '/**/Document').as('schema');
      cy.intercept('PATCH', '/**/document').as('edit');
      // Given a logged in editor
      cy.viewport('macbook-16');
      cy.createContent({
        contentType: 'Document',
        contentId: 'document',
        contentTitle: 'Test document',
      });
      cy.createContent({
        contentType: 'Event',
        contentId: 'event',
        contentTitle: 'Test Event',
      });
      cy.createContent({
        contentType: 'News Item',
        contentId: 'news-item',
        contentTitle: 'Test News Item',
      });

      cy.autologin();
    });

    it('As editor I can add head title and nav_title in breadcrumbs for page content type', function () {
      cy.visit('/document');
      cy.navigate('/document/edit');
      cy.wait('@schema');
      cy.get('#field-head_title').click().type('Custom Head Title');
      cy.get('#field-nav_title').click().type('Custom Navigation Title');
      cy.get('#toolbar-save').click();
      cy.wait('@edit');
      cy.wait('@content');
      cy.get('.breadcrumb .section').should(
        'have.text',
        'Custom Navigation Title',
      );
      cy.get('.breadcrumb').should('exist');
      cy.get('.breadcrumb .home').find('svg').should('exist');
    });
    it('As editor I can add head title and nav_title in breadcrumbs for event content type', function () {
      cy.visit('/event');
      cy.navigate('/event/edit');
      cy.wait('@content');
      cy.get('#field-head_title').click().type('Custom Head Title');
      cy.get('#field-nav_title').click().type('Custom Navigation Title');
      cy.get('#toolbar-save').click();

      cy.wait('@content');
      cy.get('.breadcrumb .section').should(
        'have.text',
        'Custom Navigation Title',
      );
      cy.get('span.head-title').should('include.text', 'Custom Head Title');
      cy.get('.breadcrumb').should('exist');
      cy.get('.breadcrumb .home').find('svg').should('exist');
    });
    it('As editor I can add head title and nav_title in breadcrumbs for news item content type', function () {
      cy.visit('/news-item');
      cy.navigate('/news-item/edit');
      cy.wait('@content');
      cy.get('#field-head_title').click().type('Custom Head Title');
      cy.get('#field-nav_title').click().type('Custom Navigation Title');
      cy.get('#toolbar-save').click();
      cy.wait('@content');
      cy.wait('@content');
      cy.get('.breadcrumb .section').should(
        'have.text',
        'Custom Navigation Title',
      );
      cy.get('span.head-title').should('include.text', 'Custom Head Title');
      cy.get('.breadcrumb').should('exist');
      cy.get('.breadcrumb .home').find('svg').should('exist');
    });

    it('As editor I can add head title and nav_title in main menu and fat menu for page content type', function () {
      cy.visit('/document');
      cy.navigate('/document/edit');
      cy.wait('@schema');
      cy.get('#field-head_title').click().type('Custom Head Title');
      cy.get('#field-nav_title').click().type('Custom Navigation Title');
      cy.get('#toolbar-save').click();
      cy.wait('@edit');
      cy.wait('@content');
      // then we are able to see main menu nav.
      cy.get('#navigation .desktop-menu li .item')
        .contains('Custom Navigation Title')
        .should('exist');
      // then we are able to see fat menu nav.
      cy.get('ul.desktop-menu button')
        .contains('Custom Navigation Title')
        .click();
      cy.get('.submenu-inner').should('exist');
      cy.get('.submenu-inner h2')
        .contains('Custom Navigation Title')
        .should('exist');
    });
    it('As editor I can add head title and nav_title in main menu and fat menu for event content type', function () {
      cy.visit('/event');
      cy.navigate('/event/edit');

      cy.wait('@content');
      cy.get('#field-head_title').click().type('Custom Head Title');
      cy.get('#field-nav_title').click().type('Custom Navigation Title');
      cy.get('#toolbar-save').click();

      cy.wait('@content');
      // then we are able to see main menu nav.
      cy.get('#navigation .desktop-menu li .item')
        .contains('Custom Navigation Title')
        .should('exist');
      cy.get('span.head-title').should('include.text', 'Custom Head Title');
      // then we are able to see fat menu nav.
      cy.get('ul.desktop-menu button')
        .contains('Custom Navigation Title')
        .click();
      cy.get('.submenu-inner').should('exist');
      cy.get('.submenu-inner h2')
        .contains('Custom Navigation Title')
        .should('exist');
    });
    it('As editor I can add head title and nav_title in main menu and fat menu for news item content type', function () {
      cy.visit('/news-item');
      cy.navigate('/news-item/edit');
      cy.wait('@content');
      cy.get('#field-head_title').click().type('Custom Head Title');
      cy.get('#field-nav_title').click().type('Custom Navigation Title');
      cy.get('#toolbar-save').click();
      cy.wait('@content');

      // then we are able to see main menu nav.
      cy.get('#navigation .desktop-menu li .item')
        .contains('Custom Navigation Title')
        .should('exist');
      cy.get('span.head-title').should('include.text', 'Custom Head Title');

      // then we are able to see fat menu nav.
      cy.get('ul.desktop-menu button')
        .contains('Custom Navigation Title')
        .click();
      cy.get('.submenu-inner').should('exist');
      cy.get('.submenu-inner h2')
        .contains('Custom Navigation Title')
        .should('exist');
    });
    it('As editor I can add nav_title fallback to title when empty for Document', function () {
      cy.visit('/document');
      cy.navigate('/document/edit');
      cy.wait('@content');
      cy.get('#field-nav_title').clear();
      cy.get('#toolbar-save').click();
      cy.get('.breadcrumb .section').should('have.text', 'Test document');
      cy.get('#navigation .desktop-menu li .item')
        .contains('Test document')
        .should('exist');
    });
    it('As editor I can add nav_title fallback to title when empty for Event', function () {
      cy.visit('/event');
      cy.navigate('/event/edit');
      cy.wait('@content');
      cy.get('#field-nav_title').clear();
      cy.get('#toolbar-save').click();
      cy.get('.breadcrumb .section').should('have.text', 'Test Event');
      cy.get('#navigation .desktop-menu li .item')
        .contains('Test Event')
        .should('exist');
    });

    it('As editor I can add nav_title fallback to title when empty for News Item', function () {
      cy.visit('/news-item');
      cy.navigate('/news-item/edit');
      cy.wait('@content');
      cy.get('#field-nav_title').clear();
      cy.get('#toolbar-save').click();
      cy.get('.breadcrumb .section').should('have.text', 'Test News Item');
      cy.get('#navigation .desktop-menu li .item')
        .contains('Test News Item')
        .should('exist');
    });
  });
});
