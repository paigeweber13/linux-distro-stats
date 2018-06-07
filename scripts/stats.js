// constants
// alias distro = distribution
const reviewPageBaseUrl = 'https://distrowatch.com/dwres.php?resource=ratings&distro=';
const distrosToCheck = ['slackware', 'fedora'];
// TODO: make custom proxy so I don't rely on someone else's
const proxyUrl = 'https://cors-anywhere.herokuapp.com/';

// global variables
// reviewPageHtml = new Map(); // map of distro names to html of review pages.
distros = []; // array of javascript objects. Objects look like comment below.
/**
 * {
 *   name:
 *   reviewsText:
 * }
 */

$( '#test-button' ).click(function() {
  getReviewsPagesHtml(distrosToCheck);
});

$('#test-python-button').click(function() {
  $.ajax({
    url: 'scripts/stats.py',
    method: 'GET',
    success: function(data) {
      console.log('success! Data is printing below.');
      console.log(data);
    },
    error: function(data) {
      console.log('Failed to get anything from the stats.py file');
    },
  });
});

/**
 * uses a CORS-anywhere proxy because chrome blocks some CORS requests
 * passes distroName as a parameter so that we can create a map later. This must
 * be done here and not in the parent function because these fire
 * asynchronously. This means that the parent function will complete the for
 * loop iterating through distribution names before any of the html data comes
 * back. Therefore, when we try to use the distro name from the for loop, we
 * will only ever use the name used in the final iteration. This would cause the
 * code to repeatedly re-assign the map for a single key instead of using the
 * proper key
 * @param {string} distroName
 * @param {string} url
 * @return {Promise}
 */
function getHtml(distroName, url) {
  return new Promise(function(resolve, reject) {
    $.ajax({
      url: proxyUrl + url,
      method: 'GET',
      success: function(data) {
        // doesn't seem to pass anything but the first parameter... distroName
        // becomes undefined ?????
        resolve(
          {
            distroName: distroName,
            reviewPageHtml: data,
          }
        );
      },
      error: function(data) {
        reject('Failed to get review page html for ' + distroName)
      },
    });
  });
}

/**
 * Gets the review data for all the given distribution names and puts them into
 * FIX THIS DESCRIPTION
 * reviewPageHtml.
 * @param {(string|array)} distroNames
 */
function getReviewsPagesHtml(distroNames) {
  getReviewPagesPromises = [];
  for (distro of distroNames) {
    getReviewPagesPromises.push(getHtml(distro, reviewPageBaseUrl + distro));
  }
  Promise.all(getReviewPagesPromises)
  .then(function(successResponse) {
    for (response of successResponse) {
      htmlArray = $($.parseHTML(response.reviewPageHtml));
      console.log('htmlArray: ', htmlArray);
      // this currently does nothing. I guess filter only works on top-level
      // objects? it doesn't check any children of the objects in this array,
      reviews = htmlArray.filter('td[width="70%"]');
      console.log('reviews: ', reviews);
      distros.push({
        name: response.distroName,
        reviewsText: reviews,
      });

      // reviewPageHtml.set(response.distroName,
      //   $($.parseHTML(response.reviewPageHtml)));
    }
    console.log(distros);
  }, function(errorResponse) {
    console.log(errorResponse);
  });
}
