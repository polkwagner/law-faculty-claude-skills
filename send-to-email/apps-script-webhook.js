/**
 * Email Attachment Webhook for Claude
 * 
 * Deploy as a Google Apps Script Web App.
 * Receives a JSON payload with a base64-encoded file and either:
 *   - AUTO-SENDS to pwagner@law.upenn.edu (hardcoded safe recipient)
 *   - Creates a DRAFT for any other recipient (safety measure)
 *
 * SETUP:
 * 1. Go to https://script.google.com and create a new project
 * 2. Paste this entire file into Code.gs (replacing any existing content)
 * 3. Click Deploy > New deployment
 * 4. Select type: "Web app"
 * 5. Set "Execute as": Me (your Google account)
 * 6. Set "Who has access": Anyone
 * 7. Click Deploy, authorize when prompted
 * 8. Copy the Web app URL
 * 9. In Claude.ai, set it as: APPS_SCRIPT_EMAIL_WEBHOOK=<your-url>
 *    (Or just paste the URL when Claude asks for it)
 *
 * PAYLOAD FORMAT:
 * {
 *   "recipient": "email@example.com",
 *   "subject": "[ claude ] Subject line",
 *   "body": "Email body text",
 *   "filename": "document.docx",
 *   "filedata": "<base64-encoded file content>"
 * }
 *
 * RESPONSE:
 * Auto-send: { "status": "ok", "action": "sent", ... }
 * Draft:     { "status": "ok", "action": "draft", "draftId": "..." }
 * Error:     { "status": "error", "message": "..." }
 */

// Addresses that get auto-sent. Everything else becomes a draft.
var AUTO_SEND_RECIPIENTS = [
  'pwagner@law.upenn.edu',
  'polk@polkwagner.com'
];

function doPost(e) {
  try {
    var payload = JSON.parse(e.postData.contents);
    
    // Validate required fields
    var required = ['recipient', 'subject', 'filename', 'filedata'];
    for (var i = 0; i < required.length; i++) {
      if (!payload[required[i]]) {
        return ContentService.createTextOutput(
          JSON.stringify({ status: 'error', message: 'Missing required field: ' + required[i] })
        ).setMimeType(ContentService.MimeType.JSON);
      }
    }
    
    // Enforce [ claude ] subject prefix
    var subject = payload.subject;
    if (subject.indexOf('[ claude ]') !== 0) {
      subject = '[ claude ] ' + subject;
    }
    
    // Decode the base64 file
    var fileBlob = Utilities.newBlob(
      Utilities.base64Decode(payload.filedata),
      getMimeType(payload.filename),
      payload.filename
    );
    
    var body = payload.body || 'Document attached — sent from Claude.';
    var recipient = payload.recipient.trim().toLowerCase();
    
    // Auto-send to allowlisted recipients; draft for anyone else
    if (AUTO_SEND_RECIPIENTS.indexOf(recipient) !== -1) {
      GmailApp.sendEmail(
        recipient,
        subject,
        body,
        { attachments: [fileBlob] }
      );
      
      return ContentService.createTextOutput(
        JSON.stringify({ 
          status: 'ok',
          action: 'sent',
          recipient: recipient,
          subject: subject,
          message: 'Email sent with attachment: ' + payload.filename
        })
      ).setMimeType(ContentService.MimeType.JSON);
      
    } else {
      var draft = GmailApp.createDraft(
        payload.recipient,
        subject,
        body,
        { attachments: [fileBlob] }
      );
      
      return ContentService.createTextOutput(
        JSON.stringify({ 
          status: 'ok',
          action: 'draft',
          recipient: payload.recipient,
          subject: subject,
          draftId: draft.getId(),
          message: 'Draft created (non-default recipient) with attachment: ' + payload.filename
        })
      ).setMimeType(ContentService.MimeType.JSON);
    }
    
  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ status: 'error', message: err.toString() })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Also handle GET requests (for testing the endpoint is live)
 */
function doGet(e) {
  return ContentService.createTextOutput(
    JSON.stringify({ 
      status: 'ok', 
      message: 'Email webhook is live. Send a POST request with file data.' 
    })
  ).setMimeType(ContentService.MimeType.JSON);
}

/**
 * Infer MIME type from filename extension
 */
function getMimeType(filename) {
  var ext = filename.split('.').pop().toLowerCase();
  var types = {
    'pdf':  'application/pdf',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'doc':  'application/msword',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'xls':  'application/vnd.ms-excel',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'ppt':  'application/vnd.ms-powerpoint',
    'html': 'text/html',
    'htm':  'text/html',
    'md':   'text/markdown',
    'txt':  'text/plain',
    'csv':  'text/csv',
    'json': 'application/json',
    'png':  'image/png',
    'jpg':  'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif':  'image/gif',
    'svg':  'image/svg+xml',
    'zip':  'application/zip'
  };
  return types[ext] || 'application/octet-stream';
}
