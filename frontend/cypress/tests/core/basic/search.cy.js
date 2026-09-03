const createDocument = ({ id, title }) => {
  cy.createContent({
    contentType: 'Document',
    contentId: id,
    contentTitle: title,
  });
};

const visitSearchResults = (searchableText) => {
  cy.visit(`/search?SearchableText=${encodeURIComponent(searchableText)}`);
  cy.get('#search-results .summary.url').should('have.length.at.least', 2);
};

const sortSearchResults = (index, order = 'ascending') => {
  cy.get(`button[name="${index}"]`).click();
  cy.wait('@search').then(({ request, response }) => {
    expect(response.statusCode).to.equal(200);

    const searchRequest = new URL(request.url);
    expect(searchRequest.searchParams.get('sort_on')).to.equal(index);
    expect(searchRequest.searchParams.get('sort_order')).to.equal(order);
  });
};

const expectFirstResults = (expectedTitles) => {
  cy.get('.summary.url').should(($results) => {
    const actualTitles = [...$results]
      .slice(0, expectedTitles.length)
      .map((result) => result.textContent.trim());

    expect(actualTitles).to.deep.equal(expectedTitles);
  });
};

describe('Search result ordering', () => {
  beforeEach(() => {
    cy.intercept('GET', '/**/@search*').as('search');
    cy.autologin();
  });

  it('ranks an exact title match before a partial title match', () => {
    createDocument({ id: 'orchid', title: 'Orchid' });
    createDocument({
      id: 'orchid-growing-handbook',
      title: 'Orchid Growing Handbook',
    });

    visitSearchResults('Orchid');

    expectFirstResults(['Orchid', 'Orchid Growing Handbook']);
  });

  it('orders results alphabetically by title', () => {
    createDocument({
      id: 'zebra-field-guide',
      title: 'Zebra Field Guide',
    });
    createDocument({
      id: 'albatross-field-guide',
      title: 'Albatross Field Guide',
    });

    visitSearchResults('Field Guide');
    sortSearchResults('sortable_title');

    expectFirstResults(['Albatross Field Guide', 'Zebra Field Guide']);
  });

  it('orders results by effective date with the newest first', () => {
    createDocument({
      id: 'older-astronomy-bulletin',
      title: 'Older Astronomy Bulletin',
    });
    createDocument({
      id: 'newer-astronomy-bulletin',
      title: 'Newer Astronomy Bulletin',
    });
    cy.setWorkflow({
      path: 'older-astronomy-bulletin',
      effective: '2020-08-13T15:58:24+00:00',
      expires: '2035-05-14T15:58:24+00:00',
    });
    cy.setWorkflow({
      path: 'newer-astronomy-bulletin',
      effective: '2024-08-15T15:58:24+00:00',
      expires: '2035-05-14T15:58:24+00:00',
    });

    visitSearchResults('Astronomy Bulletin');
    sortSearchResults('effective', 'reverse');

    expectFirstResults([
      'Newer Astronomy Bulletin',
      'Older Astronomy Bulletin',
    ]);
  });
});
