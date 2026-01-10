import React from 'react';

const ChatMessage = ({ message }) => {
    const isBot = message.sender === 'bot';

    const isDiagnosis = message.sender === 'bot' && message.treatment;

    if (isDiagnosis) {
        return (
            <div className="message-row centered-report fade-in">
                <div className="diagnosis-report-card">
                    <div className="report-header-section">
                        <div className="report-icon">🌿</div>
                        <h2 className="report-title">Diagnosis Report</h2>
                    </div>

                    <div className="diagnosis-result-section">
                        <div dangerouslySetInnerHTML={{ __html: message.text.replace(/\n/g, '<br/>') }} />
                    </div>

                    <div className="treatment-grid">
                        {message.treatment.causes && (
                            <div className="report-card causes">
                                <div className="card-icon">🔍</div>
                                <h3>Causes</h3>
                                <p>{message.treatment.causes}</p>
                            </div>
                        )}
                        {message.treatment.treatment && (
                            <div className="report-card treatment">
                                <div className="card-icon">💊</div>
                                <h3>Treatment</h3>
                                <p>{message.treatment.treatment}</p>
                            </div>
                        )}
                        {message.treatment.prevention && (
                            <div className="report-card prevention">
                                <div className="card-icon">🛡️</div>
                                <h3>Prevention</h3>
                                <p>{message.treatment.prevention}</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className={`message-row ${isBot ? 'bot' : 'user'} fade-in`}>
            <div className="message-content">
                <div className={`avatar ${isBot ? 'bot-avatar' : 'user-avatar'}`}>
                    {isBot ? '🤖' : '👤'}
                </div>
                <div className="message-bubble">
                    {message.image && (
                        <img src={message.image} alt="Uploaded" className="message-image" />
                    )}
                    {message.text && (
                        <div dangerouslySetInnerHTML={{ __html: message.text.replace(/\n/g, '<br/>') }} />
                    )}
                </div>
            </div>
        </div>
    );
};

export default ChatMessage;
