import SourceCard from "./SourceCard";

function AnswerCard({ result }) {
    if (!result) {
        return null;
    }

    return (
        <div className="answer-section">

            <h3>Answer</h3>

            <p>
                {result.answer}
            </p>

            {result.citations &&
                result.citations.length > 0 && (

                <div className="citations">

                    <h3>
                        Sources
                    </h3>

                    {result.citations.map(
                        (citation, index) => (
                            <SourceCard
                                key={
                                    citation.chunk_id ||
                                    index
                                }
                                citation={citation}
                            />
                        )
                    )}

                </div>
            )}

        </div>
    );
}

export default AnswerCard;