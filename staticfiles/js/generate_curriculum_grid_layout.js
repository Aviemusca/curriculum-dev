(function(){
/* Generates the grid layout for the curriculum detail view */

    // Grid parameters
    const numColumns = 4;                 // The number of columns in the grid (number of rows is dynamic)
    const sideBarColumnSpan = 1;          // The number of columns the side bar takes up in the grid
    const headerRowSpan = 1;              // The number of rows the header takes up in the grid
    const boxRowSpan = 2;                 // The number of rows an analysis box takes up in the grid

    // Layout functions (for the grid, header, side-bar and analysis boxes)

    const setCssVariables = () => {
    /* Sets the css variables, header properties and side-bar column properties are generated
     * in the css file from these */

        document.documentElement.style.setProperty('--num-columns', numColumns);
        document.documentElement.style.setProperty('--side-bar-column-span', sideBarColumnSpan);
        document.documentElement.style.setProperty('--header-row-span', headerRowSpan);
    };

    const setBoxRows = (box, index) => {
    /* Sets the start row and end row css properties of a curriculum analysis box within the grid */

        const rowStart = (headerRowSpan + 1) + index * boxRowSpan;
        const rowEnd = rowStart + boxRowSpan;
        box.style.setProperty('grid-row-start', rowStart);
        box.style.setProperty('grid-row-end', rowEnd);
    };

    const setHeaderRowEnd = (lastAnalysisBox) => {
    /* Sets the end row for the side bar equal to the end row of the last analysis box */

        // Get the end row of the last box
        const rowEnd = lastAnalysisBox.style.getPropertyValue('grid-row-end');

        // Set the end row of the side-bar
        const sideBar = document.getElementById('curriculum-grid-side-bar');
        sideBar.style.setProperty('grid-row-end', rowEnd);

    };

    setCssVariables();
    const analysisBoxes = Array.from(document.getElementsByClassName('curriculum-analysis-box'));
    analysisBoxes.forEach(setBoxRows);
    setHeaderRowEnd(analysisBoxes.pop());
}());
