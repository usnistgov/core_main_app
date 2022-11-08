/** Admin migration data JS **/
let taskRefreshInterval = 1000;
let jqWarning = $('.alert-warning');
let jqError = $('.alert-error');
let isAllDataSelected = false;
let isAllTemplateSelected = false;
let isTargetCreated = false;
let nextPageUrl = null;
let setStatesPending = 0;
let setStatesTargetTemplateId;
let totalDataCount = 0;
let showError = false;
let versionManagerId = null
/**
 * Init controllers for the results page
 */
$(document).ready(function() {
    // create the action button listeners
    $("#validate-button").on("click", () => { actionButtonClicked(false) });
    $("#migrate-button").on("click", () => { actionButtonClicked(true) });
    $(".back-to-version-manager").on("click", () => { backToVersionManager() });
    $(".switch-input").change(function() {
        fillTemplateList($(this).is(":checked"));
    });

    // create the listener for the select all data button
    $("#select-all-data").on("click", (event) => {
        isAllDataSelected = !isAllDataSelected;
        let dataCheckboxElement = $("#data-table").find("input[type=checkbox]");
        $(dataCheckboxElement).prop('checked', isAllDataSelected);

        if (!event.originalEvent.eventFired) {
            createTargetTemplateListHtml(isAllDataSelected);
        } else {
            // if the click is fired by a custom event force the checkbox state
            isAllDataSelected = true;
            $("#select-all-data").prop('checked', isAllDataSelected);
            let parentRowElement = $("td[data-target-template-id=" + setStatesTargetTemplateId + "]").parentsUntil('tbody')[0];
            let targetInputElement = $(parentRowElement).find('input[type=radio]')[0];
            $(targetInputElement).prop("checked", true);

            // trigger the check target template event
            eventFire(targetInputElement, 'click');

        }

        // update the data count and show xsl transformation list
        if (isAllDataSelected) {
            $(".data-count").show();
            $("#data-number").html(totalDataCount);
            viewXsltList(true)
        }
        else{
            $(".data-count").hide();
        }

    });
    // create the listener for the select all template button
    $("#select-all-template").on("click", () => {
        isAllTemplateSelected = !isAllTemplateSelected;
        let dataCheckboxElement = $("#template-table").find("input[type=checkbox]");
        $(dataCheckboxElement).prop('checked', isAllTemplateSelected);

        // launch the data request
        fillTheData(isAllTemplateSelected ? $('td[data-template-id]')
            .map(function() {
                return { id: $(this).attr("data-template-id") };
            })
            .get() : []);
    });
    // create listener for the template selection
    createTemplateListener()

    // get the fragment from url to select a predefined state if needed
    // ex. #from=1234567,12345678,1234567&to12345678&tvm=987123
    if (location.hash.substr(1) !== "") {
        // enable back to version manager button
        $(".back-to-version-manager").attr("hidden",false);

        isTargetCreated = true
        let sourceTemplates = location.hash.substr(1).split("&to=");
        let targetTemplate = sourceTemplates.pop().split("&tvm=");
        versionManagerId = targetTemplate.pop();

        sourceTemplates = sourceTemplates[0].split("from=")[1].split(",");

        if (targetTemplate && sourceTemplates && sourceTemplates.length > 0) {
            setState(sourceTemplates, targetTemplate);
        }
        else{
            console.error('An error occurred while parsing url parameters.');
        }
    }

});

/**
 * Set the migration workflow to a specific state
 * @param {Array<string>} sourceTemplates List of the source template id
 * @param {String} targetTemplate target template id
 */
let setState = function(sourceTemplates, targetTemplate) {
    sourceTemplates.forEach((id) => {
        setStatesPending += 1;
        eventFire($("td[data-template-id=" + id + "]")[0], "click");
    });

    setStatesTargetTemplateId = targetTemplate;

}

/**
 *  Get the DOM element which contain the clicked template
 *  and fill the data panel with the data which belong to
 *  the selected template
 *  @param {Array<string>} templateIdList List of the clicked template id
 */
let fillTheData = function(templateIdList) {

    jqWarning.hide();

    // reset the data count
    $("#data-number").html("0");
    $(".data-count").hide();


    if (templateIdList && templateIdList.length > 0) {
        $.ajax({
            url: loadDataUrlBase,
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ query: {}, templates: templateIdList }),
            success: (data) => {
                totalDataCount = data.count;

                createDataListHtml(data, false, "#data-table tbody");


                if (data.next) {
                    // add the infinite scroll listener
                    $("#infinite-scroll-bt").on("click", () => {
                        loadMoreData(templateIdList);
                    });

                    nextPageUrl = data.next;
                }

            },
            error: function(error) {
                jqWarning.html('Impossible to retrieve the data: ' + error.responseJSON.message);
                jqWarning.show();
            }
        });
    } else {
        $('#select-all-data').prop("disabled", true);
        dataHtml = '<tr id="empty-data-text" class="bg-transparent text-center">' +
            '<td>' +
            '<strong class="text-primary">' +
            'Please select a template.' +
            '</strong>' +
            '</td>' +
            '</tr>';
        $($("#data-table tbody")[0]).html(dataHtml);
        createDataListHtml([], false, "#data-table tbody");
        viewXsltList(false)

    }
}

/**
 *  Get the DOM element which contain template list
 *  and fill the source template panel with the list
 *  @param {boolean} isUserTemplateSelected List of the clicked template id
 */
let fillTemplateList = function(isUserTemplateSelected) {

    if (isUserTemplateSelected) TemplateUrlBase =  loadAllTemplateUrlBase
    else  TemplateUrlBase =  loadGlobalTemplateUrlBase
    $.ajax({
        url: TemplateUrlBase,
        method: "GET",
        contentType: "application/json",
        success: (data) => {
            resetState();
            let templates = []
            // format templates info
            for (var i = 0; i< data.length; i++){
                // skip disabled templates
                if(!data[i].is_disabled){
                    version_index = 1
                    versions = data[i].versions
                    // add version number
                    for (var j = 0; j< versions.length; j++){
                        templates.push(
                        {
                             "id": versions[j],
                             "title":  data[i].title+ "(version "+version_index++ +")",
                        }
                        )
                    }
                }
            }
            createTemplateListHtml(templates, "#template-table tbody");

        },
        error: function(error) {
            jqWarning.html('Impossible to retrieve the template: ' + error.responseJSON.message);
            jqWarning.show();
        }
    });

}

/**
 *  Load the Nth page of the data
 *  @param {Array<string>} templateIdList List of the clicked template id
 */
let loadMoreData = function(templateIdList) {

    // delete the more button
    $("#infinite-scroll-bt").unbind()
    $("#infinite-scroll-bt").remove()

    if (templateIdList && templateIdList.length > 0 && nextPageUrl) {
        $.ajax({
            url: nextPageUrl,
            method: "POST",
            traditional: true,
            contentType: "application/json",
            data: JSON.stringify({ query: {}, templates: templateIdList }),
            success: (data) => {
                createDataListHtml(data, true, "#data-table tbody");
                nextPageUrl = data.next;

                if (nextPageUrl) {
                    // add the infinite scroll listener
                    $("#infinite-scroll-bt").on("click", () => {
                        loadMoreData(templateIdList);
                    });
                }

                // update the selected data count
                let jqCheckedDataCheckbox = $('.data-checkbox:checkbox:checked');
                if (jqCheckedDataCheckbox.length > 0) {

                    // display this number on the DOM
                    $(".data-count").show();
                    $("#data-number").html(jqCheckedDataCheckbox.length);

                } else {
                    // hide the couter
                    $(".data-count").hide();
                }

            },
            error: function(error) {
                jqWarning.html('Impossible to retrieve the data: ' + error.responseJSON.message);
                jqWarning.show();
            },
        });
    }
}


/**
 * Get the data list and create the HTML to display it
 * @param {object} data
 * @param {boolean} append
 * @param {DOMElement} tbodySelector DOM selector where the data will be injected
 */
let createDataListHtml = function(data, append, tbodySelector) {
    let dataHtml = "";
    let results = data.results;

    if (results && results.length > 0) {

        // update the state of the all data checkbox
        $('#select-all-data').prop("disabled", false);
        isAllDataSelected = false;
        $("#select-all-data").prop('checked', isAllDataSelected);
        // create one table line per data
        for (let index = 0; index < results.length; ++index) {
            dataHtml += '<tr>' +
                '<td width="20px"><input class="data-checkbox" type="checkbox"></td>' +
                '<td data-id="' + results[index].id + '"><div>' +
                '<a href="/core-admin/data?id=' + results[index].id + '">' + results[index].title + '</a>' +
                '</div></td>' +
                '</tr>';
        }

        // add the button to show more result if next page exist
        if (data.next) {
            dataHtml += '<tr>' +
                '<td class="bt-more" colspan=2>' +
                '<span id="infinite-scroll-bt" class="circle-icon">' +
                'More' +
                '<i class="fas fa-sort-down fa-5x"/>' +
                '</span>' +
                '</td>' +
                '</tr>'
        }
    } else {
        $('#select-all-data').prop("disabled", true);
        dataHtml = '<tr id="empty-data-text" class="bg-transparent text-center">' +
            '<td>' +
            '<strong class="text-primary">' +
            'Please select a template with data on the left panel.' +
            '</strong>' +
            '</td>' +
            '</tr>';
    }

    if (append)
        $($(tbodySelector)[0]).append(dataHtml);
    else
        $($(tbodySelector)[0]).html(dataHtml);

    // create the data checkbox listener
    $(".data-checkbox").unbind();
    $(".data-checkbox").on("click", (event) => {

        // check the check all checkbox if all the data checkbox are selected
        let jqCheckedDataCheckbox = $('.data-checkbox:checkbox:checked');
        isAllDataSelected = !nextPageUrl && $('.data-checkbox:checkbox').length === jqCheckedDataCheckbox.length;
        $("#select-all-data").prop('checked', isAllDataSelected);

        if (jqCheckedDataCheckbox.length > 0) {

            // display this number on the DOM
            $(".data-count").show();
            $("#data-number").html(jqCheckedDataCheckbox.length);
            viewXsltList(true);
            if(!isTargetCreated){
                isTargetCreated = true
                createTargetTemplateListHtml(true);
            }
        } else {
            createTargetTemplateListHtml(false);
            // hide the couter
            $(".data-count").hide();
        }

    });

    // load the target template list if a pending state flag is up and if data are displayed
    createTargetTemplateListHtml(setStatesPending > 0 && results.length > 0);
}


/**
 * Handle the click actions on a data
 * @param {boolean} isDataSelected
 */
let viewXsltList = function(isDataSelected) {

    if(isDataSelected){
        $("#xslt-text").hide();
        $('#xslt-content').show();
    }
    else{
        $("#xslt-content").hide();
        $('#xslt-text').show();
        $('input[name="xslt-radio"]').prop('checked',false);
    }
    // create the radio button listener
    $(".xslt-radio").on("click", (event) => {
        // enable the clear button
        $('.xslt-clear').show();
    });
    // create the clear button listener
    $(".xslt-clear").on("click", (event) => {
        $('input[name="xslt-radio"]').prop('checked',false);
        $('.xslt-clear').hide ();
    });
}

/**
 * Get the template list and create the HTML to display it
 * @param {object} templates
 * @param {DOMElement} tbodySelector DOM selector where the templates will be injected
 */
let createTemplateListHtml = function(templates, tbodySelector) {
    let templateHtml = "";

    if (templates && templates.length > 0) {
        for (let index = 0; index < templates.length; ++index) {
            templateHtml += '<tr>' +
                '<td width="20px"><input class="template-checkbox" type="checkbox"></td>' +
                '<td data-template-id="' + templates[index].id + '">' +
                '<div>' + templates[index].title +'</div></td>' +
                '</tr>';
        }

    } else {
        $('#select-all-template').prop("disabled", true);
        templateHtml = '<tr id="empty-data-text" class="bg-transparent text-center">' +
            '<td>' +
            '<strong class="text-primary">' +
            'No Template available.' +
            '</strong>' +
            '</td>' +
            '</tr>';
    }

     $($(tbodySelector)[0]).html(templateHtml);

    // create the data checkbox listener
    createTemplateListener()
}

/**
 * Handle the click actions on a data
 * @param {boolean} isDataSelected
 */
let createTargetTemplateListHtml = function(isDataSelected) {

    let targetTemplateHtml = "";
    $('.action-button').prop("disabled", true);

    // fill the target template panel with all the unchecked template
    targetTemplateId = $('.template-checkbox:checkbox:not(:checked)')
        .map(function() {
            let parents = $(this).parentsUntil("tbody");
            let jqParent = $(parents[parents.length - 1]);
            let jpTemplateRow = $(jqParent.find("td[data-template-id]")[0]);
            let templateId = jpTemplateRow.attr("data-template-id");
            return { id: templateId, titleHtml: jpTemplateRow.html() };
        })
        .get();
    if (targetTemplateId && targetTemplateId.length > 0 && isDataSelected) {
        targetTemplateId.forEach((item, index) => {
            targetTemplateHtml += '<tr>' +
                '<td width="20px"><input class="template-radio" type="radio"></td>' +
                '<td data-target-template-id="' + item.id + '">' +
                item.titleHtml +
                '</td>' +
                '</tr>';
        });
    } else if (targetTemplateId.length === 0 || !isDataSelected) {
        isTargetCreated = false
        emptyPanelMessage = isDataSelected ? 'You have selected all the ' +
            'source templates, please uncheck at least one of them to have at least a target template.' :
            'Please select at least one data to migrate.'

        targetTemplateHtml = '<tr class="bg-transparent text-center">' +
            '<td>' +
            '<strong class="text-primary">' + emptyPanelMessage + '</strong>' +
            '</td>' +
            '</tr>';
    } else {
        jqError.html('Impossible to display the target template');
        jqError.show();
    }

    $("#target-template-text").html(targetTemplateHtml);

    // create the radio button listener
    $(".template-radio").on("click", (event) => {
        $(".template-radio").prop("checked", false);
        $(event.target).prop("checked", true);
        // enable the actions button
        $('.action-button').prop("disabled", false);
    });

    // check if a set state function is waiting for the data to be displayed
    if (setStatesPending > 0) {
        // when all the data are displayed check all of them
        // disable one pending flag
        setStatesPending -= 1;

        let jqAllDataCheckbox = $("#select-all-data");

        if (!jqAllDataCheckbox.attr('disabled')) {
            eventFire(jqAllDataCheckbox[0], "click", );
        }

    }

}
/**
 * Handle the click action for back to version manager button
 */
let backToVersionManager = function(){
    if(versionManagerId){
        window.location.href = versionManagerUrlBase.replace("version_manager_id",versionManagerId);
    }
}


let createTemplateListener = function(){
    $(".template-checkbox").unbind();

    // create listener for the template selection
    $("#template-table tr").on("click", (event) => {
        let ancestors = $(event.target).parentsUntil("tbody");
        let jqParent = $(ancestors[ancestors.length - 1]);
        // if the click is out from the input trigger the check manually
        if (event.target.tagName !== "INPUT") {
            // search the clicked checkbox input and (un)check it
            let currentCheckboxValue = jqParent.find("input[type=checkbox]")[0].checked;
            jqParent.find("input[type=checkbox]")[0].checked = !currentCheckboxValue;
        }

        let jqCheckedTemplateCheckbox = $('.template-checkbox:checkbox:checked');
        // check the check all checkbox if all the template checkbox are selected
        isAllTemplateSelected = $('.template-checkbox:checkbox').length === jqCheckedTemplateCheckbox.length;
        $("#select-all-template").prop('checked', isAllTemplateSelected);


        // free the listener before the DOM rewriting
        $("#infinite-scroll-bt").unbind();


        // find all the checked checkbox on the page extract the template id
        // from their parents and create a list with it
        fillTheData(jqCheckedTemplateCheckbox
            .map(function() {
                let parents = $(this).parentsUntil("tbody");
                let jqParent = $(parents[parents.length - 1]);
                let templateId = $(jqParent.find("td[data-template-id]")[0]).attr("data-template-id")
                return { id: templateId };
            })
            .get());
    });
}

/**
 * Handle the click actions for the migration / validation buttons
 * @param {boolean} migrate If true the migration button has been clicked if not it is a validation
 */
let actionButtonClicked = function(migrate) {
    // show the progressbar
    $(".progress-container").show();
    // set the progressbar value to 0%
    $("#migration-progress-bar").css({ "width": "0%" });

    // get the target template
    let ancestors = $(".template-radio[type=radio]:checked").parentsUntil("tbody");
    let jqParent = $(ancestors[ancestors.length - 1]);
    let targetTemplateId = $(jqParent.find("td[data-target-template-id]")[0]).attr('data-target-template-id');
    let queryData = {}
        // get the source templates OR data
    if ($("#select-all-data").prop("checked")) {
        // if the all data is checked we will get all the data from the templates
        queryData.template = extractIdFromTable(".template-checkbox:checkbox:checked",
            "td[data-template-id]",
            "data-template-id");

    } else {
        // if the all data is not checked we will get all the checked data
        queryData.data = extractIdFromTable(".data-checkbox:checkbox:checked",
            "td[data-id]",
            "data-id");
    }

    if($(".xslt-radio[type=radio]").is(':checked')){
        // get the xsl transformation
        let ancestors_xslt = $(".xslt-radio[type=radio]:checked").parentsUntil("tbody")
        let jqParent_xslt = $(ancestors_xslt[ancestors_xslt.length - 1]);
        queryData.xslt = $(jqParent_xslt.find("td[xslt-id]")[0]).attr('xslt-id');
    }

    // launch the async task
    $.ajax({
        url: migrationUrlBase
            .replace("placeholder_id", targetTemplateId)
            .replace("migrate", migrate ? "migrate" : "validate"),
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(queryData),
        dataType: "json",
        success: (taskId) => {
            let interval = setInterval(() => {
                    try {
                        getTaskStatus(taskId, (statusData) => {
                            if (statusData && statusData.state === 'SUCCESS') {
                                clearInterval(interval);
                            }
                            displaySummary(statusData, migrate);
                        }, (taskResultError) => {
                            clearInterval(interval);
                            displaySummary(taskResultError, migrate);
                        });
                    } catch (error) {
                        clearInterval(interval);
                        jqError.html('Error during the task execution: ' + JSON.stringify(error));
                        jqError.show();
                    }
                },
                taskRefreshInterval);
        },
        error: (error) => {
            jqError.html('Impossible to start the ' +
                (migrate ? 'migration' : 'validation') +
                ' task :' + (error.responseText ? error.responseText : JSON.stringify(error)));
            jqError.show();
        }
    });

}


/**
 * Extract the id according to the input tag values
 * @param {string} mainSelector table selector
 * @param {string} findSelector selector to find the attr container
 * @param {string} attrToRead name of the attr which contain the id
 */
let extractIdFromTable = function(mainSelector, findSelector, attrToRead) {
    return $(mainSelector)
        .map(function() {
            let parents = $(this).parentsUntil("tbody");
            let jqParent = $(parents[parents.length - 1]);
            let jpTemplateRow = $(jqParent.find(findSelector)[0]);
            let templateId = jpTemplateRow.attr(attrToRead);
            return templateId;
        })
        .get();
}

/**
 * Get the task status
 * @param {string} taskId
 * @param {function} success callback
 * @param {function} error callback
 */
let getTaskStatus = function(taskId, success, error) {
    $.ajax({
        url: taskBaseUrl.replace("placeholder_id", taskId),
        type: "GET",
        contentType: "application/json",
        dataType: "json",
        success: (data) => {
            success(data);
        },
        error: (err) => {
            error(err);
        }
    });
}

/**
 * Parse the task status and dispay it on the UI
 * @param {object} taskData Task status object
 * @param {boolean} migrate If true the migration button has been clicked if not it is a validation
 */
let displaySummary = function(taskData, migrate) {
    if (taskData) {
        let summaryHtml = '';
        switch (taskData.state) {
            case 'PENDING':
                // wait for the task to start
                summaryHtml = '<p>Waiting for the task to start ...</p>';
                break;
            case 'PROGRESS':

                let percentage = 0;
                // it is a template migration status structure
                if (taskData.details && taskData.details.template_total > 1) {
                    let mainTemplateProgress = parseFloat(taskData.details.template_current) / parseFloat(taskData.details.template_total);
                    let rangeMaxLimitTemplateProgress = (parseFloat(taskData.details.template_current) + 1) / parseFloat(taskData.details.template_total);
                    let range = rangeMaxLimitTemplateProgress - mainTemplateProgress;
                    let dataProgress = parseFloat(taskData.details.data_current) / parseFloat(taskData.details.data_total);
                    let dataGlobalProgress = range * dataProgress;
                    let mainGlobalProgress = mainTemplateProgress + dataGlobalProgress;

                    // update percentage
                    percentage = mainGlobalProgress * 100;

                    // update the visual task summary
                    summaryHtml = '<ul class="list-group list-group-flush">' +
                        '<li class="list-group-item">Template to process: <strong>' + taskData.details.template_total + '</strong></li>' +
                        '<li class="list-group-item">Template processed: <strong>' + taskData.details.template_current + '</strong></li>' +
                        '<li class="list-group-item">Data to process: <strong>' + taskData.details.data_total + '</strong></li>' +
                        '<li class="list-group-item">Data processed: <strong>' + taskData.details.data_current + '</strong></li>' +
                        '</ul>'
                } else if (taskData.details && taskData.details.template_total === 1) {
                    // update percentage
                    percentage = (parseFloat(taskData.details.data_current) / parseFloat(taskData.details.data_total)) * 100;
                    // update the visual task summary
                    summaryHtml = '<ul class="list-group list-group-flush">' +
                        '<li class="list-group-item">Data to process: <strong>' + taskData.details.data_total + '</strong></li>' +
                        '<li class="list-group-item">Data processed: <strong>' + taskData.details.data_current + '</strong></li>' +
                        '</ul>'
                } else if (taskData.details && taskData.details.total > 0) {
                    // update percentage
                    percentage = (parseFloat(taskData.details.current) / parseFloat(taskData.details.total)) * 100;
                    // update the visual task summary
                    summaryHtml = '<ul class="list-group list-group-flush">' +
                        '<li class="list-group-item">Data to process: <strong>' + taskData.details.total + '</strong></li>' +
                        '<li class="list-group-item">Data processed: <strong>' + taskData.details.current + '</strong></li>' +
                        '</ul>'
                } else {
                    throw 'Error when the task was running, wrong object structure: ' + JSON.stringify(taskData);
                }

                $("#migration-progress-bar").css({ "width": percentage + "%" });

                break;
            case 'SUCCESS':
                // 100% progressbar
                $("#migration-progress-bar").css({ "width": "100%" });
                // show the summary
                summaryHtml = '<p>Your task has been successfully executed ' +
                        '<strong class="text-success">' + taskData.details.valid.length + ' data succeeded</strong>.';
                let failedButtonHtml = "";
                // check if there is wrong migration
                if (taskData.details.wrong.length > 0) {
                    summaryHtml += " Some errors occurred during data validation: " +
                        '<strong class="text-danger">' + taskData.details.wrong.length + ' data failed</strong>.' +
                        " Data might not be valid for the selected target template. " +
                        "You can get more information by clicking on the button bellow.";

                    failedButtonHtml = '<button class="btn btn-secondary mb-3" type="button" onclick="toggleError()">' +
                            'View error' +
                        '</button>' +
                        '<div id="error-list" class="hidden"><h4>Failed data files:</h4>' +
                        '<ul class="error-container list-group list-group-flush">';

                    taskData.details.wrong.forEach((dataId) => {
                        failedButtonHtml += '<li class="list-group-item"><a href="/core-admin/data?id=' + dataId + '">' +
                                'Data (' + dataId + ')</a></li>';
                    });

                    failedButtonHtml += '</ul></div>';
                } else if(migrate === false) {
                    summaryHtml += ' Start the migration by clicking on the "migrate" button below.';
                }
                summaryHtml += "</p>" + failedButtonHtml;

                // reset the state only if it is a migration
                if (migrate)
                    resetState();

                break;
            default:
                // error
                jqError.html('Error during the task execution: ' + JSON.stringify(taskData));
                jqError.show();
        }
        $("#progress-text").html(summaryHtml);
    }
}

let toggleError = function() {
    let jqErrorList = $("#error-list");
    showError = !showError;

    if(jqErrorList && showError)
        jqErrorList.show();
    else
        jqErrorList.hide();
}

/**
 * Reset all the panel states and the url fragment
 */
let resetState = function() {
    window.location.hash = "";
    $("#select-all-data").prop("checked", false);
    $("#select-all-template").prop("checked", false);
    let jqCheckedTemplateCheckbox = $(".template-checkbox:checked");
    jqCheckedTemplateCheckbox.prop("checked", false);
    eventFire(jqCheckedTemplateCheckbox[0], "click");
    $('input[name="xslt-radio"]').prop('checked',false);
    $("#xslt-content").hide();
    $('#xslt-text').show();
    $('.xslt-clear').hide ();
}

/**
 * Dispatch an element event
 * @param {DOMElement} element target DOM element
 * @param {EventType} eventType type of the event
 */
let eventFire = function(element, eventType) {
    if (element && element.fireEvent) {
        element.fireEvent('on' + eventType);
    } else if (element) {
        let eventObject = document.createEvent('Events');
        eventObject.initEvent(eventType, true, false);
        eventObject.eventFired = true;
        element.dispatchEvent(eventObject);
    }
}