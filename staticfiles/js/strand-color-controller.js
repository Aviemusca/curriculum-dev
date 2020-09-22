import diversityChartRender from './curriculum_diversity_chart.js';
import hitCountChartRender from './curriculum_hit_count_chart.js';
import averageVerbsChartRender from './curriculum_average_verbs_chart.js';
import averageCategoriesChartRender from './curriculum_average_categories_chart.js';

function colorController(){
    /* A script to show the strand colours in the side-bar table and allow the user
     * to dynamically change them. The colour table column is initially filled with
     * HEX colour codes (strings) from the database. We make text and background
     * colours the same to hide the text but still have info about the colour. */

    // Grab the colour table column elements
    const colourElements = document.querySelectorAll('table.strand-table input.jscolor');

    // Use event bubbling and an event listener to the parent element of the rows(i.e the table)
    const table = document.querySelector('table.strand-table');
    table.addEventListener('change', event => {
        if (event.target.className === 'jscolor jscolor-active'){
            // get the colours
            const newColours = Array.from(colourElements).map(elem => elem.value);
            diversityChartRender(newColours);
            hitCountChartRender(newColours);
            averageVerbsChartRender(newColours);
            averageCategoriesChartRender(newColours);
            ajaxUpdateStrandColour(event.target);
        }
    })
};

function ajaxUpdateStrandColour(target){
    const updateUrl = target.getAttribute('update-url');
    const colour = target.value;
    const strandSlug = target.getAttribute('id');
    $.ajax({
        url: updateUrl,
        type: "POST",
        data: {
            'strand_slug': strandSlug,
            'colour': colour,
        },
        dataType: 'json',
        success: function(data){
            console.log('Updated successfully!')
            console.log(data);
        },
        error: function(xhr, errorMsg, error){
            console.log(xhr.status, xhr.responseText, errorMsg)
        }
    });
};

colorController();
